"""Modbus instance handling."""

import logging
from pymodbus.client.sync import ModbusTcpClient, ModbusSerialClient

_LOGGER = logging.getLogger(__name__)

class ModbusRTUInstance:
    """Modbus RTU client."""

    def __init__(self, config: dict) -> None:
        self._client = ModbusSerialClient(
            method=config.get("method", "rtu"),
            port=config.get("port"),
            baudrate=config.get("baudrate", 9600),
            parity=config.get("parity", "E"),
            stopbits=config.get("stopbits", 1),
            bytesize=config.get("bytesize", 8)
        )
        self._client.connect()

    async def read(self, address: int) -> float:
        """Read a register."""
        response = self._client.read_holding_registers(address, 2)
        if response.isError():
            _LOGGER.error("Error reading Modbus register")
            return None
        return response.registers[0]  # Adapt based on your register format

class ModbusTCPInstance:
    """Modbus TCP client."""

    def __init__(self, config: dict) -> None:
        self._client = ModbusTcpClient(
            host=config.get("address"),
            port=config.get("port", 502)
        )
        self._client.connect()

    async def read(self, address: int) -> float:
        """Read a register."""
        response = self._client.read_holding_registers(address, 2)
        if response.isError():
            _LOGGER.error("Error reading Modbus register")
            return None
        return response.registers[0]  # Adapt based on your register format
