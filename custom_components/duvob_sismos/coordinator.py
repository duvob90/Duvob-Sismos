from __future__ import annotations

import logging
import re
from datetime import timedelta
from typing import Any, Dict, Optional

from aiohttp import ClientError
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    DEFAULT_SCAN_INTERVAL_SECONDS,
    INDEX_URL,
    EVENT_URL,
)

_LOGGER = logging.getLogger(__name__)

# 1) En el índice tomamos el primer link /maps/{id} y el texto de la fecha UTC
RE_INDEX_ROW = re.compile(
    r'href="/maps/(?P<id>\d+)"[^>]*>\s*(?P<time>[\d\-:\s]+)\s*<', re.IGNORECASE
)

# 2) En el detalle extraemos Latitud, Longitud, Profundidad, Magnitud y Ref. Geográfica
RE_LAT = re.compile(r"Latitud:\s*([\-]?\d+(?:\.\d+)?)", re.IGNORECASE)
RE_LON = re.compile(r"Longitud:\s*([\-]?\d+(?:\.\d+)?)", re.IGNORECASE)
RE_DEPTH = re.compile(r"Profundidad:\s*([\-]?\d+(?:\.\d+)?)", re.IGNORECASE)
RE_MAG = re.compile(r"Magnitud:\s*([\-]?\d+(?:\.\d+)?)", re.IGNORECASE)
# Acepta: "Ref. Geográfica: ..." o "Referencia Geográfica: ..."
RE_REF = re.compile(
    r"(?:Ref(?:erencia)?\.?\s*Geogr(?:á|a)fica)\s*:\s*([^<\n\r]+)",
    re.IGNORECASE,
)

class CSNCoordinator(DataUpdateCoordinator[Optional[Dict[str, Any]]]):
    \"\"\"Coordina la descarga del último evento del CSN ShakeMaps.\"\"\"

    def __init__(self, hass: HomeAssistant) -> None:
        super().__init__(
            hass,
            logger=_LOGGER,
            name="duvob_sismos_coordinator",
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL_SECONDS),
        )
        self._session = async_get_clientsession(hass)

    async def _async_fetch_text(self, url: str) -> str:
        try:
            async with self._session.get(url, timeout=20) as resp:
                resp.raise_for_status()
                return await resp.text()
        except ClientError as err:
            raise UpdateFailed(f"HTTP error fetching {url}: {err}") from err

    async def _async_get_latest_event_id_and_time(self) -> Optional[dict]:
        html = await self._async_fetch_text(INDEX_URL)
        m = RE_INDEX_ROW.search(html)
        if not m:
            _LOGGER.debug("No se encontró fila de índice en %s", INDEX_URL)
            return None
        return {"id": m.group("id"), "time": m.group("time").strip()}

    async def _async_get_event_details(self, event_id: str) -> Optional[dict]:
        html = await self._async_fetch_text(EVENT_URL.format(event_id=event_id))

        def _grab_float(rx: re.Pattern, text: str) -> Optional[float]:
            mm = rx.search(text)
            return float(mm.group(1)) if mm else None

        def _grab_str(rx: re.Pattern, text: str) -> Optional[str]:
            mm = rx.search(text)
            return mm.group(1).strip() if mm else None

        lat = _grab_float(RE_LAT, html)
        lon = _grab_float(RE_LON, html)
        depth = _grab_float(RE_DEPTH, html)
        mag = _grab_float(RE_MAG, html)
        ref = _grab_str(RE_REF, html)

        if lat is None or lon is None:
            _LOGGER.debug("No se pudo extraer lat/lon para evento %s", event_id)
            return None

        return {
            "latitude": lat,
            "longitude": lon,
            "depth_km": depth,
            "magnitude": mag,
            "ref_geografica": ref,
        }

    async def _async_update_data(self) -> Optional[Dict[str, Any]]:
        meta = await self._async_get_latest_event_id_and_time()
        if not meta:
            return None

        details = await self._async_get_event_details(meta["id"])
        if not details:
            return None

        return {
            "event_id": meta["id"],
            "time_utc": meta["time"],
            "url": EVENT_URL.format(event_id=meta["id"]),
            **details,
        }
