"""Platform for HA-inepro-Modbus sensors."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .modbus_instance import ModbusRTUInstance, ModbusTCPInstance

_LOGGER = logging.getLogger(__name__)

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the HA-inepro-Modbus sensor platform."""
    if discovery_info is None:
        return

    sensors = hass.data.get('ha_inepro_modbus_sensors', {}).get(hass.config_entries.async_current_entry.entry_id, [])
    
    entities = [ModbusSensor(sensor) for sensor in sensors]
    add_entities(entities)

class ModbusSensor(SensorEntity):
    """Representation of a HA-inepro-Modbus sensor."""

    def __init__(self, sensor_config: dict) -> None:
        """Initialize the sensor."""
        self._name = sensor_config.get("name")
        self._address = sensor_config.get("address")
        self._unit_of_measurement = sensor_config.get("unit_of_measurement")
        self._modbus_instance = self._create_modbus_instance(sensor_config)
        self._state = None

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self) -> Any:
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self) -> str | None:
        """Return the unit of measurement."""
        return self._unit_of_measurement

    def _create_modbus_instance(self, sensor_config: dict):
        """Create and return the Modbus instance."""
        modbus_type = sensor_config.get("type")
        if modbus_type == "tcp":
            return ModbusTCPInstance(sensor_config)
        else:
            return ModbusRTUInstance(sensor_config)

    async def async_update(self) -> None:
        """Fetch new state data for this sensor."""
        self._state = await self._modbus_instance.read(self._address)
