from __future__ import annotations

from homeassistant import config_entries

from .const import DOMAIN

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Flujo: una sola instancia sin opciones."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        await self.async_set_unique_id("duvob_sismos_singleton")
        self._abort_if_unique_id_configured()
        return self.async_create_entry(title="Duvob Sismos", data={})
