# Diagnóstico analítico: migración y remesas

## Alcance

El diagnóstico usa indicadores anuales del Banco Mundial para Ecuador. Contiene
8 años con observaciones completas para las cuatro variables.

La serie migratoria representa personas nacidas en Ecuador que residen fuera del
país. Es una medida de stock disponible en intervalos de cinco años, no un flujo
anual ni una prueba de que quienes migraron envían remesas.

## Cobertura

| variable | observaciones | primer_anio | ultimo_anio |
| --- | --- | --- | --- |
| remesas_recibidas_usd | 41 | 1976 | 2025 |
| remesas_pct_pib | 41 | 1976 | 2025 |
| ecuatorianos_residentes_exterior | 8 | 1990 | 2024 |
| pib_usd | 66 | 1960 | 2025 |

## Correlaciones de Pearson

| index | remesas_recibidas_usd | remesas_pct_pib | ecuatorianos_residentes_exterior | pib_usd |
| --- | --- | --- | --- | --- |
| remesas_recibidas_usd | 1.0 | 0.428 | 0.845 | 0.876 |
| remesas_pct_pib | 0.428 | 1.0 | 0.374 | 0.09 |
| ecuatorianos_residentes_exterior | 0.845 | 0.374 | 1.0 | 0.885 |
| pib_usd | 0.876 | 0.09 | 0.885 | 1.0 |

La correlación descriptiva entre remesas recibidas y ecuatorianos residentes en
el exterior es **0.845**. Esta cifra puede reflejar tendencias de
tiempo, cambios de medición o factores comunes; no identifica una relación causal.

## Gráfico exploratorio

![Remesas y diáspora ecuatoriana](C:/Users/USER/Downloads/analisis-contexto-nacional-global/reports/charts/remesas_vs_diaspora.png)

## Requisito para una estimación causal

Antes de estimar un modelo, incorporar una serie compatible de ecuatorianos
residentes en el exterior o flujos de emigración, además de controles económicos
y una estrategia de identificación documentada.
