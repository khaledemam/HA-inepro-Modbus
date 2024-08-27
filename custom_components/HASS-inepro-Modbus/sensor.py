from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CONF_NAME
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
from .const import SENSOR_LIST, DOMAIN

class ModbusSensor(SensorEntity):
    """Representation of a Modbus sensor."""

    def __init__(self, config, slave_id):
        """Initialize the sensor."""
        self._name = f"{config['name']} ({slave_id})"
        self._unique_id = f"{config['unique_id']}_{slave_id}"
        self._device_class = config.get("device_class")
        self._state_class = config.get("state_class")
        self._precision = config.get("precision", 2)
        self._address = config["address"]
        self._input_type = config.get("input_type", "holding")
        self._count = config.get("count", 2)
        self._data_type = config.get("data_type", "float32")
        self._unit_of_measurement = config.get("unit_of_measurement")
        self._slave_id = slave_id
        self._scan_interval = config.get("scan_interval", 5)
        self._state = None
        self._client = None

    async def async_added_to_hass(self):
        """Set up the Modbus client when the entity is added to Home Assistant."""
        self._client = self.hass.data[DOMAIN]["client"]

    async def async_update(self):
        """Fetch new state data for this sensor."""
        try:
            # Read data from the Modbus device
            if self._input_type == "holding":
                result = await self.hass.async_add_executor_job(
                    self._client.read_holding_registers,
                    self._address,
                    self._count,
                    unit=self._slave_id
                )
            else:
                # Implement other input types if needed
                return

            if result.isError():
                raise Exception(f"Error reading Modbus data: {result}")

            # Decode the result based on the specified data type
            decoder = BinaryPayloadDecoder.fromRegisters(result.registers, Endian.Big)
            if self._data_type == "float32":
                self._state = round(decoder.decode_32bit_float(), self._precision)
            elif self._data_type == "int16":
                self._state = decoder.decode_16bit_int()
            elif self._data_type == "uint16":
                self._state = decoder.decode_16bit_uint()
            else:
                raise Exception(f"Unsupported data type: {self._data_type}")

        except Exception as e:
            self._state = None
            self._logger.error(f"Failed to update Modbus sensor {self._name}: {e}")

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def state(self):
        return self._state

    @property
    def device_class(self):
        return self._device_class

    @property
    def state_class(self):
        return self._state_class

    @property
    def unit_of_measurement(self):
        return self._unit_of_measurement

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    if discovery_info is None:
        return

    slave_id = discovery_info["slave_id"]
    sensors = [ModbusSensor(sensor_config, slave_id) for sensor_config in SENSOR_LIST]
    add_entities(sensors)
