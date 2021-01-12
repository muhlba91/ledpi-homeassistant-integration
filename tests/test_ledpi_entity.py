"""Test for the LED-Pi Entity."""

import pytest
from unittest.mock import MagicMock

from custom_components.ledpi import DOMAIN
from custom_components.ledpi.ledpi_entity import LedPiEntity


class TestLedPiEntity:
    @pytest.fixture
    def api(self):
        yield MagicMock()

    @pytest.fixture
    def coordinator(self):
        yield MagicMock()

    @pytest.fixture
    def entity(self, api, coordinator):
        yield LedPiEntity(api, coordinator, "name", "uuid")

    def test_icon(self, entity):
        assert entity.icon == "mdi:help"

    def test_device_info(self, entity):
        assert entity.device_info == {
            "identifiers": {(DOMAIN, "uuid")},
            "name": "name",
            "manufacturer": "LED-Pi",
            "model": "WS2801 LED",
        }
