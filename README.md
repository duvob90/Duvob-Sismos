# Duvob Sismos — Home Assistant

Integra el **último sismo** listado en el índice de [shakemaps.csn.uchile.cl](https://shakemaps.csn.uchile.cl/) como **entidad geolocalizada** en Home Assistant, visible en el **mapa**.

Atributos expuestos:
- `magnitude`
- `depth_km`
- `time_utc`
- `event_id`
- `ref_geografica`  ← referencia geográfica (p. ej. "52 km al SO de ...")
- `url`

## Instalación (HACS)

1. Copia `custom_components/duvob_sismos/` en tu carpeta `config/` o añade el repo como *Custom Repository* en HACS.
2. Reinicia Home Assistant.
3. **Add integration** → busca **Duvob Sismos**.

## Tarjeta de mapa

```yaml
type: map
geo_location_sources:
  - duvob_sismos
default_zoom: 5
dark_mode: true
```

o bien:

```yaml
type: map
entities:
  - entity: geo_location.ultimo_sismo_duvob_sismos
default_zoom: 6
dark_mode: true
```

## Notas

- Se actualiza cada 5 min.
- Si no ves el punto, espera el refresco o revisa los logs (filtra por `duvob_sismos`).
