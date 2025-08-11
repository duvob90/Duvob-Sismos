DOMAIN = "alerta_sismos"

INDEX_URL = "https://shakemaps.csn.uchile.cl/"
EVENT_URL = "https://shakemaps.csn.uchile.cl/maps/{event_id}"

DEFAULT_SCAN_INTERVAL_SECONDS = 300  # 5 min

ATTR_EVENT_ID = "event_id"
ATTR_MAG = "magnitude"
ATTR_DEPTH_KM = "depth_km"
ATTR_TIME_UTC = "time_utc"
ATTR_URL = "url"
ATTR_REF_GEO = "ref_geografica"

SOURCE = "alerta_sismos"
ENTITY_NAME = "Último sismo (Alerta Sismos)"
