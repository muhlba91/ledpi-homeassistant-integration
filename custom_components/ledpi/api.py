"""API for the LED-Pi integration."""
import logging
import sys
import webcolors
from homeassistant.components.light import ATTR_RGB_COLOR, ATTR_BRIGHTNESS
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import ATTR_LEDS, ATTR_STATE

_LOGGER = logging.getLogger(__name__)


class API:
    """API representation for a LED-Pi Light."""

    def __init__(self, hass, host):
        """Initialize the API."""
        self.hass = hass
        self.host = host
        self.verify_tls = False
        self.data = {}

    async def update(self, data=None):
        """Update the entity."""
        if data is not None:
            self.data = data
        else:
            session = async_get_clientsession(self.hass, self.verify_tls)
            try:
                async with session.get(f"http://{self.host}/api/v1/state") as response:
                    self.data = await response.json()
            except:
                _LOGGER.error(
                    "Could not fetch state from %s: %s", self.host, sys.exc_info()[0]
                )
                self.data = {}

    def is_on(self):
        """Check if the light is on."""
        if ATTR_STATE not in self.data:
            raise UnknownStateException("no_state")
        return self.data.get(ATTR_STATE) == "on"

    async def set_rgb(self, rgb_color: tuple, push=False):
        color = webcolors.rgb_to_hex(rgb_color)
        self.data[ATTR_RGB_COLOR] = color
        if push:
            await self._post_state(
                {
                    ATTR_RGB_COLOR: color,
                }
            )

    def rgb_hex_color(self):
        """Get the RGB Hex color."""
        if ATTR_RGB_COLOR not in self.data:
            raise UnknownStateException("no_rgb_hex_color")
        return self.data.get(ATTR_RGB_COLOR)

    def rgb_color(self):
        """Get the RGB color."""
        try:
            colors = webcolors.hex_to_rgb(self.rgb_hex_color())
            return [colors.red, colors.green, colors.blue]
        except:
            _LOGGER.error(
                "Could not convert HEX %s to RGB: %s",
                self.rgb_hex_color(),
                sys.exc_info()[0],
            )
            raise UnknownStateException("no_rgb_color")

    def rgb_name(self):
        """Get the RGB color name."""
        try:
            return webcolors.hex_to_name(self.rgb_hex_color())
        except:
            _LOGGER.error(
                "Could not convert HEX %s to color name: %s",
                self.rgb_hex_color(),
                sys.exc_info()[0],
            )
            raise UnknownStateException("no_rgb_name_color")

    def brightness(self):
        """Get the brightness."""
        if ATTR_BRIGHTNESS not in self.data:
            raise UnknownStateException("no_brightness")
        return self.data.get(ATTR_BRIGHTNESS)

    async def set_brightness(self, brightness: float, push=False):
        self.data[ATTR_BRIGHTNESS] = brightness
        if push:
            await self._post_state(
                {
                    ATTR_BRIGHTNESS: brightness,
                }
            )

    def leds(self):
        """Get the number of LEDs."""
        if ATTR_LEDS not in self.data:
            raise UnknownStateException("no_leds")
        return self.data.get(ATTR_LEDS)

    async def turn_on(self):
        """Turn the light on."""
        await self._post_state(
            {
                ATTR_STATE: "on",
                ATTR_BRIGHTNESS: self.brightness(),
                ATTR_RGB_COLOR: self.rgb_hex_color(),
            }
        )

    async def turn_off(self):
        """Turn the light off."""
        await self._post_state({ATTR_STATE: "off"})

    async def _post_state(self, state):
        """Post the desired state."""
        session = async_get_clientsession(self.hass, self.verify_tls)
        try:
            await session.post(f"http://{self.host}/api/v1/state", json=state)
        except:
            _LOGGER.error(
                "Could not update state for %s: %s", self.host, sys.exc_info()[0]
            )


class UnknownStateException(Exception):
    """State if the light is unknown."""

    def __init__(self, msg):
        super().__init__(msg)
        _LOGGER.error("Unknown state: %s", msg)
