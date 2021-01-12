"""Test for the LED-Pi Sensor Entities."""

import pytest
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, PERCENTAGE
from unittest.mock import MagicMock, patch

from custom_components.ledpi import DOMAIN, LEDPI_API, LEDPI_COORDINATOR
from custom_components.ledpi.sensor import (
    async_setup_entry,
    LedPiRGBSensor,
    LedPiRGBNameSensor,
    LedPiLEDsSensor,
    LedPiBrightnessSensor,
)


@patch("homeassistant.core.HomeAssistant")
@pytest.mark.asyncio
async def test_async_setup_entry(mock_hass):
    config_entry = ConfigEntry(
        1, DOMAIN, "entry", {CONF_NAME: "name"}, "source", "POLL", {}
    )

    class AsyncAddEntries:
        def __init__(self):
            self.called_async_add_entities = False

        def call(self, sensors, boolean):
            self.called_async_add_entities = True

    async_add_entries = AsyncAddEntries()

    mock_hass.data.return_value = {
        DOMAIN: {"entry_id": {LEDPI_API: None, LEDPI_COORDINATOR: None}}
    }

    await async_setup_entry(mock_hass, config_entry, async_add_entries.call)
    assert async_add_entries.called_async_add_entities


class TestLedPiRGBSensor:
    @pytest.fixture
    def api(self):
        yield MagicMock()

    @pytest.fixture
    def coordinator(self):
        yield MagicMock()

    @pytest.fixture
    def entity(self, api, coordinator):
        yield LedPiRGBSensor(api, coordinator, "name", "uuid")

    def test_icon(self, entity):
        assert entity.icon == "mdi:palette"

    def test_name(self, entity):
        assert entity.name == "name RGB Hex"

    def test_unique_id(self, entity):
        assert entity.unique_id == "uuid/RGB Hex"

    def test_state(self, api, entity):
        api.rgb_hex_color.return_value = "#ffffff"
        assert entity.state == "#ffffff"
        assert api.rgb_hex_color.called


class TestLedPiRGBNameSensor:
    @pytest.fixture
    def api(self):
        yield MagicMock()

    @pytest.fixture
    def coordinator(self):
        yield MagicMock()

    @pytest.fixture
    def entity(self, api, coordinator):
        yield LedPiRGBNameSensor(api, coordinator, "name", "uuid")

    def test_icon(self, entity):
        assert entity.icon == "mdi:chart-bubble"

    def test_name(self, entity):
        assert entity.name == "name RGB Name"

    def test_unique_id(self, entity):
        assert entity.unique_id == "uuid/RGB Name"

    def test_state(self, api, entity):
        api.rgb_name.return_value = "white"
        assert entity.state == "white"
        assert api.rgb_name.called


class TestLedPiLEDsSensor:
    @pytest.fixture
    def api(self):
        yield MagicMock()

    @pytest.fixture
    def coordinator(self):
        yield MagicMock()

    @pytest.fixture
    def entity(self, api, coordinator):
        yield LedPiLEDsSensor(api, coordinator, "name", "uuid")

    def test_icon(self, entity):
        assert entity.icon == "mdi:numeric"

    def test_name(self, entity):
        assert entity.name == "name Number of LEDs"

    def test_unique_id(self, entity):
        assert entity.unique_id == "uuid/Number of LEDs"

    def test_state(self, api, entity):
        api.leds.return_value = 10
        assert entity.state == 10
        assert api.leds.called


class TestLedPiBrightnessSensor:
    @pytest.fixture
    def api(self):
        yield MagicMock()

    @pytest.fixture
    def coordinator(self):
        yield MagicMock()

    @pytest.fixture
    def entity(self, api, coordinator):
        yield LedPiBrightnessSensor(api, coordinator, "name", "uuid")

    def test_icon(self, entity):
        assert entity.icon == "mdi:brightness-5"

    def test_name(self, entity):
        assert entity.name == "name Brightness"

    def test_unique_id(self, entity):
        assert entity.unique_id == "uuid/Brightness"

    def test_unit_of_measurement(self, entity):
        assert entity.unit_of_measurement == PERCENTAGE

    def test_state(self, api, entity):
        api.brightness.return_value = 1.0
        assert entity.state == 1.0
        assert api.brightness.called
