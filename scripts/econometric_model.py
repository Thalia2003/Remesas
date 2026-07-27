"""Diagnóstico descriptivo para las series anuales de migración y remesas.

No estima causalidad: el stock migratorio de WDI es inmigración en Ecuador y no
el número de ecuatorianos que viven en el exterior.
"""
from pathlib import Path
import argparse

import matplotlib.pyplot as plt
import pandas as pd

BLUE = "#075985"
RED = "#b91c1c"


def to_markdown(frame: pd.DataFrame, include_index: bool = False) -> str:
    display = frame.reset_index() if include_index else frame.copy()
    headers = [str(column) for column in display.columns]
    lines = ["| " + " | ".join(headers) + " |",
             "| " + " | ".join("---" for _ in headers) + " |"]
    for row in display.itertuples(index=False, name=None):
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(lines)


def build_scatter(frame: pd.DataFrame, output_path: Path) -> None:
    fig, axis = plt.subplots(figsize=(8.5, 6))
    axis.scatter(
        frame["ecuatorianos_residentes_exterior"] / 1_000,
        frame["remesas_recibidas_usd"] / 1_000_000_000,
        s=70,
        color=BLUE,
        alpha=0.9,
    )
    for row in frame.itertuples(index=False):
        axis.annotate(
            str(int(row.year)),
            (row.ecuatorianos_residentes_exterior / 1_000, row.remesas_recibidas_usd / 1_000_000_000),
            xytext=(6, 4),
            textcoords="offset points",
            fontsize=8,
        )

    if len(frame) >= 2:
        x = frame["ecuatorianos_residentes_exterior"].astype(float) / 1_000
        y = frame["remesas_recibidas_usd"].astype(float) / 1_000_000_000
        slope, intercept = pd.Series(y).cov(pd.Series(x)) / pd.Series(x).var(), y.mean() - (pd.Series(y).cov(pd.Series(x)) / pd.Series(x).var()) * x.mean()
        x_line = pd.Series([x.min(), x.max()])
        y_line = slope * x_line + intercept
        axis.plot(x_line, y_line, color=RED, linestyle="--", linewidth=1.8)

    axis.set_title("Remesas y diáspora ecuatoriana", loc="left", fontweight="bold")
    axis.set_xlabel("Ecuatorianos residentes en el exterior (miles)")
    axis.set_ylabel("Remesas recibidas (miles de millones de USD)")
    axis.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def main(input_path: Path, diaspora_path: Path, output_path: Path) -> None:
    data = pd.read_csv(input_path).sort_values("year")
    diaspora = pd.read_csv(diaspora_path)
    data = data.merge(diaspora[["year", "ecuatorianos_residentes_exterior"]], on="year", how="left")
    variables = ["remesas_recibidas_usd", "remesas_pct_pib",
                 "ecuatorianos_residentes_exterior", "pib_usd"]
    complete = data.dropna(subset=variables)
    if len(complete) < 3:
        raise ValueError("No hay suficientes años completos para el diagnóstico")

    correlation = complete[variables].corr(method="pearson")
    coverage = pd.DataFrame({
        "variable": variables,
        "observaciones": [int(data[column].notna().sum()) for column in variables],
        "primer_anio": [int(data.loc[data[column].notna(), "year"].min()) for column in variables],
        "ultimo_anio": [int(data.loc[data[column].notna(), "year"].max()) for column in variables],
    })
    coefficient = correlation.loc["remesas_recibidas_usd", "ecuatorianos_residentes_exterior"]
    chart_path = output_path.parent / "charts" / "remesas_vs_diaspora.png"
    chart_path.parent.mkdir(parents=True, exist_ok=True)
    build_scatter(complete, chart_path)
    report = f"""# Diagnóstico analítico: migración y remesas

## Alcance

El diagnóstico usa indicadores anuales del Banco Mundial para Ecuador. Contiene
{len(complete)} años con observaciones completas para las cuatro variables.

La serie migratoria representa personas nacidas en Ecuador que residen fuera del
país. Es una medida de stock disponible en intervalos de cinco años, no un flujo
anual ni una prueba de que quienes migraron envían remesas.

## Cobertura

{to_markdown(coverage)}

## Correlaciones de Pearson

{to_markdown(correlation.round(3), include_index=True)}

La correlación descriptiva entre remesas recibidas y ecuatorianos residentes en
el exterior es **{coefficient:.3f}**. Esta cifra puede reflejar tendencias de
tiempo, cambios de medición o factores comunes; no identifica una relación causal.

## Gráfico exploratorio

![Remesas y diáspora ecuatoriana]({chart_path.as_posix()})

## Requisito para una estimación causal

Antes de estimar un modelo, incorporar una serie compatible de ecuatorianos
residentes en el exterior o flujos de emigración, además de controles económicos
y una estrategia de identificación documentada.
"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print(f"Diagnóstico guardado en {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("data/processed/ecuador_migracion_remesas_anual.csv"))
    parser.add_argument("--diaspora", type=Path, default=Path("data/processed/ecuador_diaspora_un.csv"))
    parser.add_argument("--output", type=Path, default=Path("reports/diagnostico_anual.md"))
    args = parser.parse_args()
    main(args.input, args.diaspora, args.output)
