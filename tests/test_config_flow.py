"""Test for the LED-Pi Light Entity."""

import pytest
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_SCAN_INTERVAL
from unittest.mock import patch

from custom_components.ledpi.config_flow import LedPiFlowHandler


class TestLedPiFlowHandler:
    @patch("custom_components.ledpi.config_flow.LedPiFlowHandler.async_show_form")
    @pytest.mark.asyncio
    async def test_async_step_init_without_data(self, mock_async_show_form):
        config_flow = LedPiFlowHandler()
        await config_flow.async_step_init(None)
        assert mock_async_show_form.called

    @patch("custom_components.ledpi.config_flow.LedPiFlowHandler.async_create_entry")
    @patch("custom_components.ledpi.config_flow.LedPiFlowHandler.async_abort")
    @patch(
        "custom_components.ledpi.config_flow.LedPiFlowHandler._async_endpoint_existed"
    )
    @pytest.mark.asyncio
    async def test_async_step_init_with_data_exists(
        self, mock_async_endpoint_existed, mock_async_abort, mock_async_create_entry
    ):
        config_flow = LedPiFlowHandler()
        await config_flow.async_step_init(
            {CONF_HOST: "host", CONF_NAME: "name", CONF_SCAN_INTERVAL: 10}
        )
        assert mock_async_endpoint_existed.called
        assert mock_async_abort.called
        assert not mock_async_create_entry.called

    @patch("custom_components.ledpi.config_flow.LedPiFlowHandler.async_create_entry")
    @patch("custom_components.ledpi.config_flow.LedPiFlowHandler.async_abort")
    @patch(
        "custom_components.ledpi.config_flow.LedPiFlowHandler._async_endpoint_existed"
    )
    @pytest.mark.asyncio
    async def test_async_step_init_with_data(
        self, mock_async_endpoint_existed, mock_async_abort, mock_async_create_entry
    ):
        mock_async_endpoint_existed.return_value = False

        config_flow = LedPiFlowHandler()
        await config_flow.async_step_init(
            {CONF_HOST: "host", CONF_NAME: "name", CONF_SCAN_INTERVAL: 10}
        )
        assert mock_async_endpoint_existed.called
        assert not mock_async_abort.called
        assert mock_async_create_entry.called
