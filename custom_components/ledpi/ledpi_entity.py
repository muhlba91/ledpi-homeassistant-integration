"""The Raspberry Pi WS2801 LED Controller integration."""

from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator

from .api import API
from .const import DOMAIN


class LedPiEntity(CoordinatorEntity):
    """Representation of a LED Pi entity."""

    def __init__(self, api: API, coordinator: DataUpdateCoordinator, name: str, uuid: str):
        """Initialize a LedPi entity."""
        super().__init__(coordinator)
        self.api = api
        self._name = name
        self._uuid = uuid

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:help"

    @property
    def device_info(self):
        """Return the device information of the entity."""
        return {
            "identifiers": {(DOMAIN, self._uuid)},
            "name": self._name,
            "manufacturer": "LED-Pi",
            "model": "WS2801 LED"
        }
