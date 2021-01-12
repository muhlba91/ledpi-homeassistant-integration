"""Sensors for the LED-Pi LED-Pi integration."""
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import DiscoveryInfoType
from typing import Optional, Callable

from .const import DOMAIN, LEDPI_API, LEDPI_COORDINATOR
from .ledpi_entity import LedPiEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: Callable,
    discovery_info: Optional[DiscoveryInfoType] = None,
):
    """Set up the LED-Pi sensor platform."""
    name = entry.data[CONF_NAME]
    data = hass.data[DOMAIN][entry.entry_id]

    sensors = [
        LedPiRGBSensor(data[LEDPI_API], data[LEDPI_COORDINATOR], name, entry.entry_id),
        LedPiRGBNameSensor(
            data[LEDPI_API], data[LEDPI_COORDINATOR], name, entry.entry_id
        ),
        LedPiLEDsSensor(data[LEDPI_API], data[LEDPI_COORDINATOR], name, entry.entry_id),
        LedPiBrightnessSensor(
            data[LEDPI_API], data[LEDPI_COORDINATOR], name, entry.entry_id
        ),
    ]
    _LOGGER.debug("adding ledpi sensor entities")
    async_add_entities(sensors, True)


class LedPiRGBSensor(LedPiEntity):
    """LED-Pi Color Sensor."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._name} RGB Hex"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return f"{self._uuid}/RGB Hex"

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:palette"

    @property
    def state(self):
        """Return the current value."""
        return self.api.rgb_hex_color()


class LedPiRGBNameSensor(LedPiEntity):
    """LED-Pi Color Sensor."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._name} RGB Name"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return f"{self._uuid}/RGB Name"

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:chart-bubble"

    @property
    def state(self):
        """Return the current value."""
        return self.api.rgb_name()


class LedPiLEDsSensor(LedPiEntity):
    """LED-Pi Number of LEDs Sensor."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._name} Number of LEDs"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return f"{self._uuid}/Number of LEDs"

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:numeric"

    @property
    def state(self):
        """Return the current value."""
        return self.api.leds()


class LedPiBrightnessSensor(LedPiEntity):
    """LED-Pi Brightness Sensor."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._name} Brightness"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return f"{self._uuid}/Brightness"

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:brightness-5"

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return PERCENTAGE

    @property
    def state(self):
        """Return the current value."""
        return self.api.brightness()
