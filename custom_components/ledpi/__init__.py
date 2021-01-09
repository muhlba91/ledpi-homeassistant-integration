"""The LED-Pi Raspberry Pi WS2801 LED Controller integration."""
import asyncio
import logging
import voluptuous as vol
from datetime import timedelta
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.debounce import Debouncer
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import API
from .const import DOMAIN, LEDPI_API, LEDPI_COORDINATOR

_LOGGER = logging.getLogger(__name__)

LEDPI_SCHEMA = vol.Schema(
    vol.All(
        {
            vol.Required(CONF_NAME): cv.string,
            vol.Required(CONF_HOST): cv.string,
            vol.Required(CONF_SCAN_INTERVAL): cv.positive_int,
        },
    )
)

CONFIG_SCHEMA = vol.Schema(
    {DOMAIN: vol.Schema(vol.All(cv.ensure_list, [LEDPI_SCHEMA]))},
    extra=vol.ALLOW_EXTRA,
)

PLATFORMS = ("light", "sensor")


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up LED-Pi component via configuration.yaml."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up LED-Pi from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    name = entry.data[CONF_NAME]
    host = entry.data[CONF_HOST]
    scan_interval = entry.data[CONF_SCAN_INTERVAL]

    _LOGGER.debug("Setting up %s integration with host %s as %s", DOMAIN, host, name)

    led_api = API(hass, host)
    await led_api.update()

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=name,
        update_method=led_api.update,
        update_interval=timedelta(minutes=scan_interval),
        request_refresh_debouncer=Debouncer(hass, _LOGGER, cooldown=0, immediate=True),
    )

    hass.data[DOMAIN][entry.entry_id] = {
        LEDPI_API: led_api,
        LEDPI_COORDINATOR: coordinator,
    }

    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform),
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
            ]
        )
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
