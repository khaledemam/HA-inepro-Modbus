from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from pymodbus.client.sync import ModbusTcpClient
import logging

# Set up a logger for this integration
_LOGGER = logging.getLogger(__name__)

DOMAIN = "modbus_integration"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Modbus Integration from a config entry."""
    # Retrieve and validate necessary configuration data
    host = entry.data.get("host")
    port = entry.data.get("port", 502)  # Default Modbus TCP port
    slave_id = entry.data.get("slave_id")
    
    if not host or slave_id is None:
        _LOGGER.error("Missing 'host' or 'slave_id' in configuration")
        return False
    
    # Initialize the Modbus client
    try:
        modbus_client = ModbusTcpClient(host, port)
        if not modbus_client.connect():
            _LOGGER.error("Failed to connect to Modbus server")
            return False
    except Exception as e:
        _LOGGER.error(f"Error initializing Modbus client: {e}")
        return False

    # Store the Modbus client and configuration data in hass.data
    hass.data[DOMAIN] = {
        "client": modbus_client,
        "slave_id": slave_id,
    }
    
    # Set up platforms based on the configuration
    await hass.config_entries.async_setup_platforms(entry, ["sensor"])
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    if unload_ok:
        # Ensure we safely remove the domain data and close the client connection
        modbus_client = hass.data.get(DOMAIN, {}).get("client")
        if modbus_client:
            modbus_client.close()
        hass.data.pop(DOMAIN, None)
    return unload_ok
