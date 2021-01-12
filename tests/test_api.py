"""Test for the LED-Pi API."""

import pytest
import sys
from unittest.mock import MagicMock, Mock

mock_aiohttp_session = MagicMock()
mock_aiohttp_client = MagicMock()
mock_aiohttp_client.async_get_clientsession.return_value = mock_aiohttp_session
sys.modules["homeassistant.helpers.aiohttp_client"] = mock_aiohttp_client

from homeassistant.components.light import ATTR_RGB_COLOR, ATTR_BRIGHTNESS

from custom_components.ledpi import API
from custom_components.ledpi.api import UnknownStateException
from custom_components.ledpi.const import ATTR_STATE, ATTR_LEDS


class TestAPI:
    @pytest.fixture
    def api(self):
        yield API(None, "host")

    def test_is_on(self, api):
        api.data[ATTR_STATE] = "on"
        assert api.is_on()

    def test_is_on_off(self, api):
        api.data[ATTR_STATE] = "off"
        assert not api.is_on()

    def test_is_on_no_state(self, api):
        with pytest.raises(UnknownStateException):
            api.is_on()

    def test_rgb_hex_color(self, api):
        api.data[ATTR_RGB_COLOR] = "#ffffff"
        assert api.rgb_hex_color() == "#ffffff"

    def test_rgb_hex_color_no_state(self, api):
        with pytest.raises(UnknownStateException):
            api.rgb_hex_color()

    def test_rgb_color(self, api):
        api.data[ATTR_RGB_COLOR] = "#ffffff"
        assert api.rgb_color() == [255, 255, 255]

    def test_rgb_color_invalid(self, api):
        api.data[ATTR_RGB_COLOR] = "#xxxxxx"
        with pytest.raises(UnknownStateException):
            api.rgb_color()

    def test_rgb_color_no_state(self, api):
        with pytest.raises(UnknownStateException):
            api.rgb_color()

    def test_rgb_name(self, api):
        api.data[ATTR_RGB_COLOR] = "#ffffff"
        assert api.rgb_name() == "white"

    def test_rgb_color_name(self, api):
        api.data[ATTR_RGB_COLOR] = "#xxxxxx"
        with pytest.raises(UnknownStateException):
            api.rgb_name()

    def test_rgb_name_no_state(self, api):
        with pytest.raises(UnknownStateException):
            api.rgb_name()

    @pytest.mark.asyncio
    async def test_set_rgb(self, api):
        await api.set_rgb((255, 255, 255))
        assert api.data[ATTR_RGB_COLOR] == "#ffffff"

    @pytest.mark.asyncio
    async def test_set_rgb_invalid_color(self, api):
        await api.set_rgb((-1000, -1000, -1000))
        assert ATTR_RGB_COLOR not in api.data[ATTR_RGB_COLOR]

    @pytest.mark.asyncio
    async def test_set_rgb_push(self, api):
        await api.set_rgb((255, 255, 255), True)
        mock_aiohttp_session.post.assert_called_with(
            "http://host/api/v1/state",
            json={
                ATTR_RGB_COLOR: "#ffffff",
            },
        )

    @pytest.mark.asyncio
    async def test_set_rgb_push_http_error(self, api):
        mock_aiohttp_session.post.side_effect = Mock(side_effect=Exception("error"))
        await api.set_rgb((255, 255, 255), True)
        assert mock_aiohttp_session.post.called

    def test_brightness(self, api):
        api.data[ATTR_BRIGHTNESS] = 1.0
        assert api.brightness() == 1.0

    def test_brightness_no_state(self, api):
        with pytest.raises(UnknownStateException):
            api.brightness()

    @pytest.mark.asyncio
    async def test_set_brightness(self, api):
        await api.set_brightness(1.0)
        assert api.data[ATTR_BRIGHTNESS] == 1.0

    @pytest.mark.asyncio
    async def test_set_brightness_push(self, api):
        await api.set_brightness(1.0, True)
        mock_aiohttp_session.post.assert_called_with(
            "http://host/api/v1/state",
            json={
                ATTR_BRIGHTNESS: 1.0,
            },
        )

    @pytest.mark.asyncio
    async def test_set_brightness_push_http_error(self, api):
        mock_aiohttp_session.post.side_effect = Mock(side_effect=Exception("error"))
        await api.set_brightness(1.0, True)
        assert mock_aiohttp_session.post.called

    def test_leds(self, api):
        api.data[ATTR_LEDS] = 1
        assert api.leds() == 1

    def test_leds_no_state(self, api):
        with pytest.raises(UnknownStateException):
            api.leds()

    @pytest.mark.asyncio
    async def test_turn_on(self, api):
        api.data = {ATTR_STATE: "off", ATTR_BRIGHTNESS: 1.0, ATTR_RGB_COLOR: "#ffffff"}
        await api.turn_on()
        mock_aiohttp_session.post.assert_called_with(
            "http://host/api/v1/state",
            json={ATTR_STATE: "on", ATTR_BRIGHTNESS: 1.0, ATTR_RGB_COLOR: "#ffffff"},
        )

    @pytest.mark.asyncio
    async def test_turn_on_http_error(self, api):
        api.data = {ATTR_STATE: "off", ATTR_BRIGHTNESS: 1.0, ATTR_RGB_COLOR: "#ffffff"}
        mock_aiohttp_session.post.side_effect = Mock(side_effect=Exception("error"))
        await api.turn_on()
        assert mock_aiohttp_session.post.called

    @pytest.mark.asyncio
    async def test_turn_off(self, api):
        await api.turn_off()
        mock_aiohttp_session.post.assert_called_with(
            "http://host/api/v1/state",
            json={
                ATTR_STATE: "off",
            },
        )

    @pytest.mark.asyncio
    async def test_turn_off_http_error(self, api):
        mock_aiohttp_session.post.side_effect = Mock(side_effect=Exception("error"))
        await api.turn_off()
        assert mock_aiohttp_session.post.called

    @pytest.mark.asyncio
    async def test_update_with_data(self, api):
        await api.update({ATTR_LEDS: 10})
        assert not mock_aiohttp_session.get.called
        assert api.data[ATTR_LEDS] == 10

    @pytest.mark.asyncio
    async def test_update(self, api):
        mock_response = MagicMock()
        mock_response.json.return_value = {ATTR_LEDS: 10}
        mock_aiohttp_session.get.return_value = mock_response
        await api.update()
        mock_aiohttp_session.get.assert_called_with("http://host/api/v1/state")
        assert api.data != {}

    @pytest.mark.asyncio
    async def test_update_http_error(self, api):
        api.data = {ATTR_LEDS: 10}
        mock_aiohttp_session.get.side_effect = Mock(side_effect=Exception("error"))
        await api.update()
        mock_aiohttp_session.get.assert_called_with("http://host/api/v1/state")
        assert api.data == {}
