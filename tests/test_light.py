"""Test for the LED-Pi Light Entity."""

import pytest
from homeassistant.components.light import (
    SUPPORT_BRIGHTNESS,
    SUPPORT_COLOR,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from unittest.mock import MagicMock, AsyncMock, patch

from custom_components.ledpi import DOMAIN, LEDPI_API, LEDPI_COORDINATOR
from custom_components.ledpi.light import LedPi, async_setup_entry


@patch("homeassistant.core.HomeAssistant")
@patch("homeassistant.helpers.entity_platform.current_platform")
@pytest.mark.asyncio
async def test_async_setup_entry(mock_current_platform, mock_hass):
    config_entry = ConfigEntry(
        1, DOMAIN, "entry", {CONF_NAME: "name"}, "source", "POLL", {}
    )

    class AsyncAddEntries:
        def __init__(self):
            self.called_async_add_entities = False

        def call(self, lights, boolean):
            self.called_async_add_entities = True

    async_add_entries = AsyncAddEntries()

    mock_hass.data.return_value = {
        DOMAIN: {"entry_id": {LEDPI_API: None, LEDPI_COORDINATOR: None}}
    }

    mock_platform = MagicMock()
    mock_current_platform.get.return_value = mock_platform

    await async_setup_entry(mock_hass, config_entry, async_add_entries.call)
    assert async_add_entries.called_async_add_entities
    assert mock_current_platform.get.called
    assert mock_platform.async_register_entity_service.called


class TestLedPi:
    @pytest.fixture
    def api(self):
        yield MagicMock()

    @pytest.fixture
    def coordinator(self):
        yield MagicMock()

    @pytest.fixture
    def async_api(self):
        yield AsyncMock()

    @pytest.fixture
    def async_coordinator(self):
        yield AsyncMock()

    @pytest.fixture
    def entity(self, api, coordinator):
        yield LedPi(api, coordinator, "name", "uuid")

    @pytest.fixture
    def async_entity(self, async_api, async_coordinator):
        yield LedPi(async_api, async_coordinator, "name", "uuid")

    def test_icon(self, entity):
        assert entity.icon == "mdi:lightbulb"

    def test_name(self, entity):
        assert entity.name == "name"

    def test_unique_id(self, entity):
        assert entity.unique_id == "uuid/Light"

    def test_is_on(self, api, entity):
        api.is_on.return_value = True
        assert entity.is_on
        assert api.is_on.called

    def test_brightness(self, api, entity):
        api.brightness.return_value = 1.0
        assert entity.brightness == 1.0
        assert api.brightness.called

    def test_supported_features(self, entity):
        assert entity.supported_features == SUPPORT_BRIGHTNESS & SUPPORT_COLOR

    @pytest.mark.asyncio
    async def test_async_turn_on(self, async_api, async_coordinator, async_entity):
        await async_entity.async_turn_on(brightness=0.5, rgb_color=[255, 255, 255])
        async_api.set_brightness.assert_called_with(0.5)
        async_api.set_rgb.assert_called_with((255, 255, 255))
        assert async_api.turn_on.called
        assert async_coordinator.async_request_refresh.called

    @pytest.mark.asyncio
    async def test_async_turn_off(self, async_api, async_coordinator, async_entity):
        await async_entity.async_turn_off()
        assert async_api.turn_off.called
        assert async_coordinator.async_request_refresh.called

    @pytest.mark.asyncio
    async def test_async_set_rgb_color(
        self, async_api, async_coordinator, async_entity
    ):
        await async_entity.async_set_rgb_color([255, 255, 255])
        async_api.set_rgb.assert_called_with((255, 255, 255), True)
        assert async_coordinator.async_request_refresh.called

    @pytest.mark.asyncio
    async def test_async_set_brightness(
        self, async_api, async_coordinator, async_entity
    ):
        await async_entity.async_set_brightness(0.5)
        async_api.set_brightness.assert_called_with(0.5, True)
        assert async_coordinator.async_request_refresh.called
