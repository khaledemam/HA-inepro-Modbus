DOMAIN = "modbus_integration"

SENSOR_LIST = [
    {
        "name": "Voltage",
        "unique_id": "V",
        "device_class": "voltage",
        "state_class": "measurement",
        "precision": 2,
        "address": 0x5000,
        "input_type": "holding",
        "count": 2,
        "data_type": "float32",
        "unit_of_measurement": "V",
        "scan_interval": 5
    },
    {
        "name": "L1 Voltage",
        "unique_id": "L1V",
        "device_class": "voltage",
        "state_class": "measurement",
        "precision": 2,
        "address": 0x5002,
        "input_type": "holding",
        "count": 2,
        "data_type": "float32",
        "unit_of_measurement": "V",
        "scan_interval": 5
    },
    # Add the rest of your sensors here...
]
