from __future__ import annotations

from typing import Any, Optional

from homeassistant.components.geo_location import GeolocationEvent
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    SOURCE,
    ENTITY_NAME,
    ATTR_EVENT_ID,
    ATTR_MAG,
    ATTR_DEPTH_KM,
    ATTR_TIME_UTC,
    ATTR_URL,
    ATTR_REF_GEO,
)
from .coordinator import CSNCoordinator

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator: CSNCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([LastQuakeEntity(coordinator)], update_before_add=True)

class LastQuakeEntity(GeolocationEvent):
    """Evento geolocalizado para el último sismo."""

    _attr_name = ENTITY_NAME
    _attr_unique_id = "duvob_sismos_last_quake"

    def __init__(self, coordinator: CSNCoordinator) -> None:
        self._coordinator = coordinator
        self._data: dict[str, Any] | None = None

    async def async_update(self) -> None:
        await self._coordinator.async_request_refresh()
        self._data = self._coordinator.data

    @property
    def should_poll(self) -> bool:
        return True

    @property
    def source(self) -> str:
        return SOURCE

    @property
    def latitude(self) -> Optional[float]:
        return None if not self._data else self._data.get("latitude")

    @property
    def longitude(self) -> Optional[float]:
        return None if not self._data else self._data.get("longitude")

    @property
    def icon(self) -> str:
        return "mdi:earthquake"

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        if not self._data:
            return None
        return {
            ATTR_EVENT_ID: self._data.get("event_id"),
            ATTR_TIME_UTC: self._data.get("time_utc"),
            ATTR_MAG: self._data.get("magnitude"),
            ATTR_DEPTH_KM: self._data.get("depth_km"),
            ATTR_REF_GEO: self._data.get("ref_geografica"),
            ATTR_URL: self._data.get("url"),
        }
