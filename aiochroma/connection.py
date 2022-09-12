"""Connection module"""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Callable

import aiohttp

from .const import CREDENTIALS, DEFAULT_PORT, DEFAULT_SLEEP, HEADERS, URL, URL_MAIN
from .error import ChromaResultError

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

        self._identity: dict[str, str] = ""
        self._connected: bool = False
        self._sid: int | None = None

    ### SEND REQUESTS ->

    async def async_request(
        self,
        endpoint: str,
        method: Callable,
        payload: str = "",
        interval: float = DEFAULT_SLEEP,
    ) -> dict[str, Any]:
        """Send a request"""

        json_body = {}

        url = URL.format(
            self._host,
            self._port,
            endpoint if not self._sid else f"sid={self._sid}/{endpoint}",
        )

        try:
            async with method(url=url, headers=HEADERS, data=payload, ssl=True) as r:
                json_body = await r.json()

            if "result" in json_body and json_body["result"] != 0:
                raise ChromaResultError(json_body["result"])

            await self.async_sleep(interval)

            return json_body
        except Exception as ex:
            raise ex

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
        return result["tick"]

    @property
    def connected(self) -> bool:
        """Connection status"""

        return self._connected

    @property
    def sid(self) -> int:
        """Session ID"""

        return self._sid

    @property
    def identity(self) -> str:
        """API version"""

        return self._identity
