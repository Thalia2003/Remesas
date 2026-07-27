# Diccionario de datos

| Variable | Definición | Unidad | Fuente inicial |
| --- | --- | --- | --- |
| `remesas_recibidas_usd` | Remesas personales recibidas | USD corrientes | Banco Mundial, `BX.TRF.PWKR.CD.DT` |
| `remesas_pct_pib` | Remesas personales recibidas respecto del PIB | Porcentaje | Banco Mundial, `BX.TRF.PWKR.DT.GD.ZS` |
| `stock_migrantes_internacionales` | Personas nacidas en otro país que residen en Ecuador | Personas | Banco Mundial, `SM.POP.TOTL` |
| `pib_usd` | Producto interno bruto | USD corrientes | Banco Mundial, `NY.GDP.MKTP.CD` |

`stock_migrantes_internacionales` representa inmigración hacia Ecuador, no el
stock de ecuatorianos residentes en el exterior. No debe usarse como denominador
de las remesas recibidas ni interpretarse como una medida de emigración.

## Datos mensuales del BCE (fase de integración)

La descarga mensual se conserva sin alterar y se perfila antes de limpiar. La
salida normalizada tendrá `fecha`, `remesas_usd` y, cuando las columnas estén
publicadas, `pais_origen` y `provincia_destino`. Los nombres originales de las
variables del BCE se registran mediante argumentos del script para mantener
trazabilidad.
