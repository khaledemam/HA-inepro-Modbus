"""Config flow for HA-inepro-Modbus integration."""

from typing import Any, Dict

from homeassistant import config_entries
import voluptuous as vol

from .const import DOMAIN

class ModbusConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for HA-inepro-Modbus integration."""

    VERSION = 1

    async def async_step_user(self, user_input: Dict[str, Any] = None) -> config_entries.FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=self._get_schema()
            )

        # Process the input and validate
        return self.async_create_entry(
            title=user_input['name'],
            data={
                "name": user_input['name'],
                "address": user_input['address'],
                "port": user_input['port'],
                "type": user_input['type'],
                'sensors': self._get_sensors()  # Retrieve or configure sensors
            }
        )

    def _get_schema(self):
        """Return the schema for the configuration form."""
        return vol.Schema({
            vol.Required('name'): str,
            vol.Required('address'): str,
            vol.Required('port'): int,
            vol.Required('type', default="serial"): vol.In(["serial", "tcp"]),
        })

    def _get_sensors(self):
        """Return or configure sensors."""
        # This is a placeholder. You would configure sensors based on user input or predefined settings.
        return []
