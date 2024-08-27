"""Platform for Modbus integration."""
from __future__ import annotations

import logging
import voluptuous as vol
from typing import Any, Dict, Union

from .modbus_instance import ModbusRTUInstance, ModbusTCPInstance
from pprint import pformat

# Import the device class from the component that you want to support
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant.const import CONF_NAME, CONF_ADDRESS, CONF_PORT, CONF_TYPE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

_LOGGER = logging.getLogger("modbus")

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME): cv.string,
    vol.Required(CONF_ADDRESS): cv.string,
    vol.Optional(CONF_PORT, default=502): cv.port,  # Default port for Modbus TCP
    vol.Required(CONF_TYPE): vol.In(["tcp", "serial"]),
})


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the Modbus Sensor platform."""
    _LOGGER.info(pformat(config))
    
    modbus_device = {
        "name": config.get(CONF_NAME),
        "address": config[CONF_ADDRESS],
        "port": config[CONF_PORT],
        "type": config[CONF_TYPE]
    }
    
    add_entities([ModbusSensor(modbus_device, sensor) for sensor in hass.data[config.get(CONF_NAME)]])


class ModbusSensor(SensorEntity):
    """Representation of a Modbus Sensor."""

    def __init__(self, modbus_device: Dict[str, Any], sensor_config: Dict[str, Any]) -> None:
        """Initialize a ModbusSensor."""
        _LOGGER.info(pformat(modbus_device))
        self._name = sensor_config["name"]
        self._unique_id = sensor_config["unique_id"]
        self._device_class = sensor_config["device_class"]
        self._state_class = sensor_config["state_class"]
        self._precision = sensor_config["precision"]
        self._address = sensor_config["address"]
        self._input_type = sensor_config["input_type"]
        self._count = sensor_config["count"]
        self._data_type = sensor_config["data_type"]
        self._unit_of_measurement = sensor_config["unit_of_measurement"]
        self._slave = sensor_config["slave"]
        self._scan_interval = sensor_config["scan_interval"]

        # Initialize the Modbus connection
        if modbus_device["type"] == "tcp":
            self._device = ModbusTCPInstance(modbus_device["address"], modbus_device["port"])
        elif modbus_device["type"] == "serial":
            self._device = ModbusRTUInstance(modbus_device["address"])
        else:
            raise ValueError(f"Unsupported Modbus type: {modbus_device['type']}")
        
        self._state = None
        self._attributes = {
            "unit_of_measurement": self._unit_of_measurement,
            "device_class": self._device_class,
            "state_class": self._state_class,
            "precision": self._precision
        }

    @property
    def name(self) -> str:
        """Return the display name of this sensor."""
        return self._name

    @property
    def unique_id(self) -> str:
        """Return a unique ID for this sensor."""
        return self._unique_id

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def device_class(self) -> str:
        """Return the device class of this sensor."""
        return self._device_class

    @property
    def state_class(self) -> str:
        """Return the state class of this sensor."""
        return self._state_class

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return self._unit_of_measurement

    def update(self) -> None:
        """Fetch new state data for this sensor."""
        try:
            response = self._device.read_register(self._address, self._count, self._data_type, self._slave)
            if self._data_type == "float32":
                # Example conversion for 32-bit float
                import struct
                self._state = struct.unpack('>f', response)[0]
            else:
                self._state = response
        except Exception as e:
            _LOGGER.error(f"Error reading Modbus data: {e}")
            self._state = None
