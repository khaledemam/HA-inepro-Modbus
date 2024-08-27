"""The HA-inepro-Modbus integration component for Home Assistant."""

from __future__ import annotations

import logging
from typing import Any, Dict

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .modbus_instance import ModbusRTUInstance, ModbusTCPInstance

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the HA-inepro-Modbus integration."""
    _LOGGER.info("Setting up HA-inepro-Modbus integration")
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up HA-inepro-Modbus from a config entry."""
    _LOGGER.info(f"Setting up HA-inepro-Modbus entry: {entry.entry_id}")

    modbus_device = {
        "name": entry.data.get("name"),
        "address": entry.data.get("address"),
        "port": entry.data.get("port"),
        "type": entry.data.get("type")
    }

    # Store the sensors in hass.data to be used by the platform setup
    hass.data.setdefault('ha_inepro_modbus_sensors', {})[entry.entry_id] = entry.data.get('sensors', [])

    # Register the sensors
    hass.config_entries.async_setup_platform(entry, 'sensor')

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a HA-inepro-Modbus config entry."""
    _LOGGER.info(f"Unloading HA-inepro-Modbus entry: {entry.entry_id}")

    # Unload the platform
    hass.config_entries.async_unload_platforms(entry, ['sensor'])

    # Remove the stored sensors
    hass.data['ha_inepro_modbus_sensors'].pop(entry.entry_id, None)

    return True
