"""The Modbus integration component for Home Assistant."""

from __future__ import annotations

import logging
from typing import Any, Dict

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, CONF_ADDRESS, CONF_PORT, CONF_TYPE
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.typing import ConfigType

from .modbus_instance import ModbusRTUInstance, ModbusTCPInstance

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Modbus integration."""
    _LOGGER.info("Setting up Modbus integration")
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Modbus from a config entry."""
    _LOGGER.info(f"Setting up Modbus entry: {entry.entry_id}")

    modbus_device = {
        "name": entry.data.get(CONF_NAME),
        "address": entry.data.get(CONF_ADDRESS),
        "port": entry.data.get(CONF_PORT),
        "type": entry.data.get(CONF_TYPE)
    }

    # Load sensors defined in the configuration entry
    sensors = entry.data.get('sensors', [])
    
    # Store the sensors in hass.data to be used by the platform setup
    hass.data.setdefault('modbus_sensors', {})[entry.entry_id] = sensors

    # Register the sensors
    hass.config_entries.async_setup_platform(entry, 'sensor')

    # Optionally handle device and entity registry if needed
    # device_registry = dr.async_get(hass)
    # entity_registry = er.async_get(hass)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a Modbus config entry."""
    _LOGGER.info(f"Unloading Modbus entry: {entry.entry_id}")

    # Unload the platform
    hass.config_entries.async_unload_platforms(entry, ['sensor'])

    # Remove the stored sensors
    hass.data['modbus_sensors'].pop(entry.entry_id, None)

    return True
