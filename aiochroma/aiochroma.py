"""AIOChroma module"""

from __future__ import annotations

import json
import logging
from typing import Any

import aiohttp

from .connection import Connection
from .const import (
    CHROMA_EFFECT,
    CHROMA_KEYBOARD_HEIGHT,
    CHROMA_KEYBOARD_WIDTH,
    CHROMA_PARAM,
    CHROMA_TARGETS,
    DEFAULT_BRIGHTNESS,
    DEFAULT_COLOR,
    DEFAULT_SLEEP,
    DEFAULT_SPACING,
    EFFECT_CUSTOM,
    EFFECT_NONE,
    EFFECT_STATIC,
    KEY_CODES,
    KEY_HEADSET,
    KEY_KEYBOARD,
    KEY_KEYPAD,
    KEY_LINK,
    KEY_MOUSE,
    KEY_MOUSEPAD,
    KEYREG,
    LAYOUT,
)
from .dataclass import Color
from .error import ChromaUnknownLayout, ChromaUnknownTarget, ChromaWrongParameter

_LOGGER = logging.getLogger(__name__)


class AIOChroma:
    """AIOChroma class"""

    def __init__(
        self,
        host: str,
        targets: list["str"],
        layout: str,
        session: aiohttp.ClientSession | None = None,
    ):
        """Initialize AIOChroma module"""

        if layout in LAYOUT:
            self._layout = LAYOUT[layout].copy()
        else:
            raise ChromaUnknownLayout(layout)

        self._connection: Connection = Connection(host, session=session)
        self._connected: bool = False

        self._state: dict[str, dict[str, Any]] = dict()

        for target in targets:
            if target in CHROMA_TARGETS:
                self._state[target] = dict()
                self._state[target]["brightness"] = DEFAULT_BRIGHTNESS
                self._state[target]["color"] = DEFAULT_COLOR
                self._state[target]["state"] = True

        self._state_keyboard: list[list[int]] = [
            [0 for i in range(CHROMA_KEYBOARD_WIDTH)]
            for j in range(CHROMA_KEYBOARD_HEIGHT)
        ]

    async def async_initialize(
        self, targets: list[str], color: Color = DEFAULT_COLOR
    ) -> bool:
        """Initialize devices"""

        for target in targets:
            if not target in CHROMA_TARGETS:
                raise ChromaUnknownTarget(target)

            await self.async_effect_color(target=target, color=color)
            _LOGGER.debug(f"Target `{target}` initialized")

    async def async_connect(self) -> bool:
        """Connect to Chroma"""

        # Identify first
        await self._connection.async_identify()

        # Connect
        self._connected = await self._connection.async_connect()

        # Because this is the only way to connect completely
        if self._connected:
            await self.async_keep()
            await self.async_keep()

        return self._connected

    async def async_keep(self) -> None:
        """Keep connection"""

        await self._connection.async_keep()

    async def async_disconnect(self) -> None:
        """Disconnect"""

        await self._connection.async_disconnect()
        self._connected = False

    ### EFFECTS -->

    async def async_effect_none(
        self, target: str, sleep: float = DEFAULT_SLEEP
    ) -> None:
        """Send none message"""

        if target not in CHROMA_TARGETS:
            raise ChromaUnknownTarget(target)

        payload = json.dumps(
            {
                CHROMA_EFFECT: EFFECT_NONE,
            }
        )

        await self._connection.async_put(
            endpoint=target, payload=payload, interval=sleep
        )
        await self.async_save_state(target=target, state=False)

    async def async_effect_color(
        self,
        target: str,
        color: Color | None = None,
        brightness: int | None = None,
        sleep: float = DEFAULT_SLEEP,
    ) -> None:
        """Single color effect"""

        if target not in CHROMA_TARGETS:
            raise ChromaUnknownTarget(target)

        if not brightness:
            brightness = self._state[target]["brightness"]
        if not color:
            color = self._state[target]["color"]

        payload = json.dumps(
            {
                CHROMA_EFFECT: EFFECT_STATIC,
                CHROMA_PARAM: color.scale(brightness).as_int(),
            }
        )

        await self._connection.async_put(
            endpoint=target, payload=payload, interval=sleep
        )
        await self.async_save_state(
            target=target, color=color, brightness=brightness, state=True
        )

    async def async_effect_blink(
        self,
        target: str,
        color: Color | None = None,
        brightness: int | None = None,
        repeats: int = 1,
        spacing: float = DEFAULT_SPACING,
    ) -> None:
        """Blink effect"""

        if target not in CHROMA_TARGETS:
            raise ChromaUnknownTarget(target)

        while repeats:
            await self.async_effect_none(target=target, sleep=spacing)
            await self.async_effect_color(
                target=target, color=color, brightness=brightness, sleep=spacing
            )

            repeats -= 1

        await self.async_effect_none(target=target, sleep=spacing)

    async def async_effect_keyboard(
        self, effect: list[list[int]], spacing: float = DEFAULT_SPACING
    ) -> None:
        """Keyboard by key effect"""

        payload = json.dumps(
            {
                CHROMA_EFFECT: EFFECT_CUSTOM,
                CHROMA_PARAM: effect,
            }
        )
        await self._connection.async_put(
            endpoint=KEY_KEYBOARD, payload=payload, interval=spacing
        )

        await self.async_save_state_keyboard(effect)

    ### <-- EFFECTS

    ### KEYBOARD -->

    async def async_parse_message(self, message) -> list[str]:
        """Parse message"""

        key_sp = dict()
        keys = list()

        # Find special keys
        for match in KEYREG.finditer(message):
            key_sp[match.start()] = match.group()

        # List the sequence of keys to use
        i = 0
        while i < len(message):
            if i in key_sp:
                keys.append(key_sp[i].replace("{", "").replace("}", ""))
                i += len(key_sp[i])
            else:
                keys.append(message[i])
                i += 1

        return keys

    async def async_set_keyboard_key(
        self,
        effect: list[list[int]],
        keys: list[str] | str,
        color: Color,
        brightness: int | None = None,
    ) -> list[list[int]]:
        """Set keyboard key value"""

        if type(keys) == str:
            keys = [keys]

        for item in keys:
            code = KEY_CODES[item]
            effect[code.row][code.column] = color.scale(brightness).as_int()

        return effect

    async def async_keyboard_sequence(
        self,
        message: str,
        color: Color = DEFAULT_COLOR,
        background: int = 0,
        brightness: int | None = None,
        tail: int = 0,
        repeats: int = 1,
        spacing: float = DEFAULT_SPACING,
        sleep: float = DEFAULT_SLEEP,
    ) -> None:
        """Send a key sequence"""

        _LOGGER.debug(
            f"Starting `keyboard_seqyence` with message=`{message}`, color=`{color}`, background=`{background}`, brightness=`{brightness}`, tail=`{tail}`, repeats=`{repeats}`, spacing=`{spacing}`, sleep=`{sleep}`"
        )

        # Get previous keyboard state
        was = self._state["keyboard"].copy()
        _LOGGER.debug(f"Previous keyboard state: {was}")

        # Parse the message
        keys = await self.async_parse_message(message)

        # Set background
        await self.async_effect_color(
            target=KEY_KEYBOARD, color=background, brightness=brightness
        )

        length = len(keys)
        # Don't allow tail longer than message
        if tail >= length:
            tail = length - 1
        while repeats:
            el = 0

            while el < length:
                effect = self._state_keyboard
                if keys[el] in self._layout:
                    # Turn off tail end
                    rudiment = el - tail - 1
                    if rudiment < length:
                        effect = await self.async_set_keyboard_key(
                            effect=effect,
                            keys=self._layout[keys[rudiment]],
                            color=background,
                            brightness=brightness,
                        )
                    effect = await self.async_set_keyboard_key(
                        effect=effect,
                        keys=self._layout[keys[el]],
                        color=color,
                        brightness=brightness,
                    )
                else:
                    _LOGGER.warning(f"Key '{keys[el]}' is unknown")
                    continue

                await self.async_effect_keyboard(effect=effect, spacing=spacing)

                el += 1

            repeats -= 1

            # Get rid of the tail in the end
            if repeats < 1:
                while el < length + tail + 1:
                    # Turn off tail end
                    rudiment = el - tail - 1
                    if rudiment > -1:
                        effect = await self.async_set_keyboard_key(
                            effect=effect,
                            keys=self._layout[keys[rudiment]],
                            color=background,
                            brightness=brightness,
                        )

                    await self.async_effect_keyboard(effect=effect, spacing=spacing)

                    el += 1

        # Recover previous state
        _LOGGER.debug(f"Recovering keyboard state: {was}")
        if was["state"]:
            await self.async_effect_color(
                target="keyboard", color=was["color"], brightness=was["brightness"]
            )
        else:
            await self.async_effect_none(target="keyboard")

    ### <-- KEYBOARD

    ### ACTIONS -->

    async def async_turn_off(self, target: str = "") -> None:
        """Turn off the target."""

        if not target in CHROMA_TARGETS:
            raise ChromaUnknownTarget(target)

        await self.async_effect_none(target=target)

        return

    async def async_turn_on(
        self,
        target: str = "",
        color: Color | None = None,
        brightness: int | None = None,
    ) -> None:
        """Turn on the target."""

        _LOGGER.debug(
            f"Received command turn_on with target=`{target}`, color=`{color}`, brightness=`{brightness}`"
        )

        if not target in CHROMA_TARGETS:
            raise ChromaUnknownTarget(target)

        if brightness is not None:
            if brightness > 255 or brightness < 0:
                raise ChromaWrongParameter(f"Wrong `brightness` value `{brightness}`")
            color = self._state[target]["color"]
            # _LOGGER.debug(
            #     f"Original color: r=`{color.r}`, g=`{color.g}`, b=`{color.b}`, brightness=`{color.brigtness()}`"
            # )

            # # Scale to new brightn
            # ratio = brightness / color.brigtness()
            # new_color = color.scale(ratio)

            # _LOGGER.debug(
            #     f"New color: r=`{new_color.r}`, g=`{new_color.g}`, b=`{new_color.b}`, brightness=`{new_color.brigtness()}`"
            # )

        elif color is None:
            color = self._state[target]["color"]

        await self.async_effect_color(target=target, color=color, brightness=brightness)

        return

    ### <-- ACTIONS

    ### STATES -->

    async def async_get_state(self, target: str = "") -> bool:
        """Get state of the target"""

        # Keep alive if asking
        await self.async_keep()

        if target == str():
            return self._state

        if not target in CHROMA_TARGETS:
            raise ChromaUnknownTarget(target)

        return self._state[target]

    async def async_save_state(
        self,
        target: str,
        color: Color | None = None,
        brightness: int | None = None,
        state: bool | None = None,
    ) -> None:
        """Save state of the target"""

        if not target in CHROMA_TARGETS:
            raise ChromaUnknownTarget(target)

        if color:
            if type(color) != Color:
                raise ValueError(f"Wrong color `{color}` of type `{type(color)}`")
            self._state[target]["color"] = color
            self._state[target]["state"] = True

        if brightness:
            if type(brightness) != int:
                raise ValueError(
                    f"Wrong state `{brightness}` of type `{type(brightness)}`"
                )
            self._state[target]["brightness"] = brightness
            self._state[target]["state"] = True

        if state is not None:
            if type(state) != bool:
                raise ValueError(f"Wrong state `{state}` of type `{type(state)}`")
            self._state[target]["state"] = state

    async def async_save_state_keyboard(self, state: list[list[int]] | int = 0) -> None:
        """Save state of target"""

        if (
            type(state) == list
            and len(state) == CHROMA_KEYBOARD_HEIGHT
            and type(state[0]) == list
            and len(state[0]) == CHROMA_KEYBOARD_WIDTH
        ):
            self._state_keyboard = state
            return

        # Save the color
        if type(state) == int:
            self._state_keyboard = [
                [state for i in range(CHROMA_KEYBOARD_WIDTH)]
                for j in range(CHROMA_KEYBOARD_HEIGHT)
            ]
        else:
            raise ValueError(f"Wrong value `{state}` of type `{type(state)}`")

    ### <-- STATES

    @property
    def identity(self) -> dict[str, str]:
        """Chroma versions"""

        return self._connection.identity
