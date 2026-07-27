# Migración y remesas en Ecuador

Base reproducible para estudiar la evolución de las remesas recibidas por Ecuador
y su relación descriptiva con la migración internacional. El alcance inicial es
anual, nacional y comparable internacionalmente; la siguiente fase incorpora la
desagregación mensual, provincial y por país de origen publicada por el BCE.

## Flujo inicial

```powershell
python -m pip install -r requirements.txt
python scripts/download_data.py
python scripts/clean_data.py
python scripts/validate_data.py
python scripts/calculate_indicators.py
python scripts/download_un_diaspora.py
python scripts/import_un_diaspora.py --input data/raw/un_migrant_stock_by_origin.xlsx --sheet-name "Table 1" --header-row 10 --origin-column "Region, development group, country or area"
python scripts/econometric_model.py
```

Los archivos generados se guardan en `data/raw` y `data/processed` (ambos
ignorados por Git). El descargador consulta la API pública del Banco Mundial para
Ecuador; no se distribuyen datos descargados dentro del repositorio.

## Alcance y cautela analítica

Las remesas recibidas y el stock de migrantes internacionales no miden el mismo
universo poblacional. Por ello, los indicadores producidos describen tendencias
paralelas y no prueban causalidad ni calculan "remesa por migrante". Las
definiciones y limitaciones están en `docs/diccionario_datos.md`.

## Próxima ampliación

Integrar la publicación del BCE para remesas de trabajadores, con la debida
homologación metodológica antes y después del cambio de esquema de julio de 2025.

### Datos mensuales del BCE

```powershell
python scripts/download_bce_remesas.py
python scripts/profile_bce_remesas.py
python scripts/clean_bce_remesas.py
python scripts/generate_charts.py
python scripts/generate_report.py
```

### Serie de ecuatorianos residentes en el exterior

Descarga e importa la serie oficial de Naciones Unidas:

El limpiador usa las columnas vigentes del BCE (`anio`, `mes`, `monto_USD`,
`descr_tipo_transaccion`, `descr_pais` y `descr_provincia`) y conserva solo
remesas recibidas. Sus nombres se pueden reemplazar mediante argumentos si el
esquema publicado cambia.

El diagnóstico anual genera también un gráfico exploratorio en
`reports/charts/remesas_vs_diaspora.png`.
# Remesas
# Remesas
