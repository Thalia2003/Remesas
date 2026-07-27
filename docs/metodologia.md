# Metodología

1. Descargar cuatro indicadores anuales del Banco Mundial para Ecuador.
2. Normalizar a una fila por año y una columna por indicador.
3. Validar unicidad del año, tipos numéricos y valores faltantes en remesas.
4. Calcular variación interanual de remesas y de PIB, y expresar remesas en miles
   de millones de USD.
5. Interpretar resultados como análisis descriptivo. Cualquier modelo causal
   requerirá hipótesis, controles, estrategia de identificación y series
   compatibles sobre emigración ecuatoriana.

La siguiente fase añadirá series del BCE. El cambio metodológico anunciado para
julio de 2025 obliga a documentar rupturas de serie antes de comparar periodos.

Para la fuente mensual del BCE el procedimiento es: descargar la base original,
inspeccionar sus columnas, declarar explícitamente la columna de fecha y monto,
normalizar los montos y agregar por mes. Si se usan provincia o país de origen,
estos se conservan como dimensiones, no como supuestos de causalidad.
