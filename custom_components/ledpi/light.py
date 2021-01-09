"""Light entity for the LED-Pi light."""
import homeassistant.helpers.config_validation as cv
import logging
import voluptuous as vol
from homeassistant.components.light import (
    LightEntity,
    SUPPORT_BRIGHTNESS,
    SUPPORT_COLOR,
    ATTR_BRIGHTNESS,
    ATTR_RGB_COLOR,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_platform
from homeassistant.helpers.typing import DiscoveryInfoType
from typing import Optional, Callable

from .const import (
    DOMAIN,
    LEDPI_API,
    LEDPI_COORDINATOR,
    SERVICE_SET_RGB_COLOR,
    SERVICE_SET_BRIGHTNESS,
)
from .ledpi_entity import LedPiEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: Callable,
    discovery_info: Optional[DiscoveryInfoType] = None,
):
    """Set up the LED-Pi light platform."""
    name = entry.data[CONF_NAME]
    data = hass.data[DOMAIN][entry.entry_id]

    lights = [
        LedPi(
            data[LEDPI_API],
            data[LEDPI_COORDINATOR],
            name,
            entry.entry_id,
        )
    ]
    async_add_entities(lights, True)

    # register service
    platform = entity_platform.current_platform.get()
    platform.async_register_entity_service(
        SERVICE_SET_RGB_COLOR,
        {
            vol.Required(ATTR_RGB_COLOR): cv.ensure_list,
        },
        "async_set_rgb_color",
    )
    platform.async_register_entity_service(
        SERVICE_SET_BRIGHTNESS,
        {
            vol.Required(ATTR_BRIGHTNESS): cv.small_float,
        },
        "async_set_brightness",
    )


class LedPi(LedPiEntity, LightEntity):
    """LED-Pi Light."""

    @property
    def name(self):
        """Return the display name of the light."""
        return self._name

    @property
    def unique_id(self):
        """Return the unique id of the light."""
        return f"{self._uuid}/Light"

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:lightbulb"

    @property
    def is_on(self):
        """Return if the service is on."""
        return self.api.is_on()

    @property
    def brightness(self):
        """Return the brightness of the light."""
        return self.api.brightness()

    @property
    def supported_features(self):
        """Flag supported features."""
        return SUPPORT_BRIGHTNESS & SUPPORT_COLOR

    async def async_turn_on(self, **kwargs):
        """Instruct the light to turn on."""
        if ATTR_BRIGHTNESS in kwargs:
            self.api.set_brightness(float(kwargs.get(ATTR_BRIGHTNESS)))
        if ATTR_RGB_COLOR in kwargs:
            await self.api.set_rgb(tuple(kwargs.get(ATTR_RGB_COLOR)))
        await self.api.turn_on()
        await self.async_update()

    async def async_turn_off(self, **kwargs):
        """Instruct the light to turn off."""
        await self.api.turn_off()
        await self.async_update()

    async def async_set_rgb_color(self, rgb_color: list):
        await self.api.set_rgb(tuple(rgb_color), True)
        await self.async_update()

    async def async_set_brightness(self, brightness: float):
        await self.api.set_brightness(brightness, True)
        await self.async_update()
