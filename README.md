# Alerta Sismos — Home Assistant

Integra el **último sismo** listado en el índice de [shakemaps.csn.uchile.cl](https://shakemaps.csn.uchile.cl/) como **entidad geolocalizada** en Home Assistant, visible en el **mapa**.

Atributos expuestos:
- `magnitude`
- `depth_km`
- `time_utc`
- `event_id`
- `ref_geografica`  ← referencia geográfica (por ejemplo: "52 km al SO de ...")
- `url`

## Instalación (HACS)

1. Copia `custom_components/alerta_sismos/` en tu `config/` o añade el repo como *Custom Repository*.
2. Reinicia Home Assistant.
3. **Add integration** → “Alerta Sismos”.

## Tarjeta de mapa

```yaml
type: map
geo_location_sources:
  - alerta_sismos
default_zoom: 5
dark_mode: true
```

o bien:

```yaml
type: map
entities:
  - entity: geo_location.ultimo_sismo_alerta_sismos
default_zoom: 6
dark_mode: true
```

## Notas

- Se actualiza cada 5 min.
- Si no ves el punto, espera el refresco o revisa los logs.
