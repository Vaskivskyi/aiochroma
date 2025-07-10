"""Connection module"""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any, Callable, Optional

import aiohttp

from aiochroma.const import CREDENTIALS, DEFAULT_PORT, DEFAULT_SLEEP, HEADERS, URL_MAIN
from aiochroma.error import ChromaError, ChromaResultError

_LOGGER = logging.getLogger(__name__)


class Connection:
    """AIOChroma connection"""

    def __init__(
        self,
        host: str,
        port: int = DEFAULT_PORT,
        session: aiohttp.ClientSession | None = None,
    ):
        """Properties for connection"""

        self._host = host
        self._port = port
        self._session: aiohttp.ClientSession = (
            session if session else aiohttp.ClientSession()
        )

        self._identity: dict[str, str] = {}
        self._connected: bool = False
        self._sid: int | None = None

    ### ------------------------
    ### Service methods -->
    ### ------------------------

    def _mark_disconnected(self) -> None:
        """Mark connection as disconnected."""

        self._connected = False

    ### ------------------------
    ### <-- Service methods
    ### ------------------------

    ### SEND REQUESTS ->

    async def async_request(
        self,
        endpoint: str,
        method: Callable,
        payload: str = "",
        interval: float = DEFAULT_SLEEP,
    ) -> dict[str, Any]:
        """Send a request"""

        # Check that we are connected
        if not self._connected and endpoint != URL_MAIN:
            if not await self.async_connect():
                raise ChromaError("Cannot connect to Chroma SDK")

        if self._sid is None:
            url = f"http://{self._host}:{self._port}/{endpoint}"
        else:
            url = f"http://{self._host}:{self._sid}/chromasdk/{endpoint}"

        try:
            async with method(
                url=url, headers=HEADERS, data=payload, ssl=False
            ) as response:
                responce_status = response.status
                if responce_status == 404:
                    raise ChromaError("Chroma SDK is not available")

                # Debug: Get raw response text first
                raw_text = await response.text()
                _LOGGER.debug(f"Raw response for {endpoint}: {raw_text}")
                
                try:
                    json_body = json.loads(raw_text)
                except (json.JSONDecodeError, ValueError) as json_ex:
                    _LOGGER.error(f"Failed to parse JSON response for {endpoint}: {raw_text}")
                    raise ChromaError(f"Invalid JSON response from Chroma SDK: {raw_text}") from json_ex

                if "result" in json_body and json_body["result"] != 0:
                    raise ChromaResultError(json_body["result"])

                await self.async_sleep(interval)

                return json_body

        except aiohttp.ClientConnectorError as ex:
            self._mark_disconnected()
            raise ChromaError("Cannot connect to the Chroma SDK") from ex

        except Exception as ex:
            self._mark_disconnected()
            raise ChromaError("Error communicating with the Chroma SDK") from ex

    async def async_delete(
        self,
        endpoint: str = "",
        payload: str = "",
        interval: float = DEFAULT_SLEEP,
    ) -> dict[str, Any]:
        """Send DELETE request"""

        return await self.async_request(
            endpoint, self._session.delete, payload, interval
        )

    async def async_get(
        self,
        endpoint: str,
        payload: str = "",
        interval: float = DEFAULT_SLEEP,
    ) -> dict[str, Any]:
        """Send GET request"""

        return await self.async_request(endpoint, self._session.get, payload, interval)

    async def async_post(
        self,
        endpoint: str,
        payload: str = "",
        interval: float = DEFAULT_SLEEP,
    ) -> dict[str, Any]:
        """Send POST request"""

        return await self.async_request(endpoint, self._session.post, payload, interval)

    async def async_put(
        self,
        endpoint: str,
        payload: str = "",
        interval: float = DEFAULT_SLEEP,
    ):
        """Send PUT request"""

        return await self.async_request(endpoint, self._session.put, payload, interval)

    ### <- SEND REQUESTS

    async def async_sleep(self, interval: float = DEFAULT_SLEEP) -> None:
        """Timeout"""

        await asyncio.sleep(interval)

    async def async_identify(self) -> None:
        """Identify Chroma API"""

        if not self._identity and not self._connected:
            result = await self.async_get(URL_MAIN)
            if "version" in result:
                self._identity = result
                _LOGGER.debug(f"Identity collected: {self._identity}")
            else:
                print(result)
                _LOGGER.warning("Cannot collect identity")

    async def async_connect(self) -> bool:
        """Connect to Chroma"""

        result = await self.async_post(URL_MAIN, CREDENTIALS)
        if "sessionid" in result:
            self._sid = int(result["sessionid"])
            self._connected = True
            return True
        return False

    async def async_disconnect(self) -> None:
        """Disconnect from Chroma"""

        await self.async_delete()

    async def async_keep(self) -> int:
        """Keep connection active"""

        result = await self.async_put("heartbeat")
        
        # Debug: Log the actual result to see what we're getting
        _LOGGER.debug(f"Heartbeat result: {result}")
        
        # Check if result is a dict before trying to access it
        if isinstance(result, dict):
            if "tick" in result:
                return result["tick"]
            else:
                _LOGGER.error(f"No 'tick' key in heartbeat response: {result}")
                raise ChromaError("Invalid heartbeat response - missing 'tick' field")
        else:
            _LOGGER.error(f"Heartbeat response is not a dict: {type(result)} - {result}")
            raise ChromaError(f"Invalid heartbeat response type: {type(result)}")

    @property
    def connected(self) -> bool:
        """Connection status"""

        return self._connected

    @property
    def sid(self) -> Optional[int]:
        """Session ID"""

        return self._sid

    @property
    def identity(self) -> dict[str, str]:
        """API version"""

        return self._identity
