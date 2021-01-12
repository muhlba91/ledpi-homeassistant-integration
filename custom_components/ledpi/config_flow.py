"""Config flow for LED-Pi integration."""
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_SCAN_INTERVAL

from .const import DOMAIN

AUTH_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST, default="10.0.150.192"): cv.string,
        vol.Required(CONF_NAME, default="ledpi"): cv.string,
        vol.Required(CONF_SCAN_INTERVAL, default=5): cv.positive_int,
    }
)


class LedPiFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for LED-Pi."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle a flow initiated by the user."""
        return await self.async_step_init(user_input)

    async def async_step_import(self, user_input=None):
        """Handle a flow initiated by import."""
        return await self.async_step_init(user_input, is_import=True)

    async def async_step_init(self, user_input, is_import=False):
        """Handle init step of a flow."""
        if user_input is not None:
            host = user_input[CONF_HOST]
            name = user_input[CONF_NAME]
            scan_interval = user_input[CONF_SCAN_INTERVAL]

            if await self._async_endpoint_existed(host):
                return self.async_abort(reason="already_configured")

            return self.async_create_entry(
                title=name,
                data={
                    CONF_HOST: host,
                    CONF_NAME: name,
                    CONF_SCAN_INTERVAL: scan_interval,
                },
            )

        errors = {}

        return self.async_show_form(
            step_id="user",
            data_schema=AUTH_SCHEMA,
            errors=errors,
        )

    async def _async_endpoint_existed(self, host):
        existing_hosts = [
            f"{entry.data.get(CONF_HOST)}" for entry in self._async_current_entries()
        ]
        return host in existing_hosts
