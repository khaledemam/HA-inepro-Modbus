import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN

# Define a configuration flow handler for the Modbus Integration
class ModbusConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Modbus Integration."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="Modbus Device", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("host"): str,
                vol.Required("port", default=502): int,
                vol.Required("slave_id"): int,
                vol.Required("baudrate", default=9600): int,
                vol.Required("parity", default="N"): vol.In(["N", "E", "O"]),
                vol.Optional("stopbits", default=1): vol.All(int, vol.Range(min=1, max=2)),
            })
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Return the options flow handler."""
        return ModbusOptionsFlowHandler(config_entry)

class ModbusOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options for Modbus Integration."""

    def __init__(self, config_entry):
        """Initialize options flow handler."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Handle the options step."""
        if user_input is not None:
            return self.async_create_entry(title="Modbus Options", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional("baudrate", default=self.config_entry.options.get("baudrate", 9600)): int,
                vol.Optional("parity", default=self.config_entry.options.get("parity", "N")): vol.In(["N", "E", "O"]),
                vol.Optional("stopbits", default=self.config_entry.options.get("stopbits", 1)): vol.All(int, vol.Range(min=1, max=2)),
            })
        )
