"""Genera un informe descriptivo reproducible desde la base mensual del BCE."""
from pathlib import Path
import argparse

import pandas as pd


def format_usd(value: float) -> str:
    return f"USD {value:,.2f}"


MONTHS_ES = ("enero", "febrero", "marzo", "abril", "mayo", "junio",
             "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre")


def table_markdown(frame: pd.DataFrame, amount_column: str = "remesas_usd") -> str:
    display = frame.copy()
    display[amount_column] = display[amount_column].map(format_usd)
    if "fecha" in display:
        display["fecha"] = pd.to_datetime(display["fecha"]).dt.strftime("%Y-%m")
    if "variacion_mensual_pct" in display:
        display["variacion_mensual_pct"] = display["variacion_mensual_pct"].map(
            lambda value: "—" if pd.isna(value) else f"{value:.2f}%"
        )
    headers = [str(column) for column in display.columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in display.itertuples(index=False, name=None):
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(lines)


def main(input_path: Path, output_path: Path, top_n: int = 10) -> None:
    data = pd.read_csv(input_path, parse_dates=["fecha"])
    required = {"fecha", "pais_origen", "provincia_destino", "remesas_usd"}
    missing = required - set(data.columns)
    if missing:
        raise ValueError(f"Faltan columnas para el informe: {', '.join(sorted(missing))}")

    monthly = (data.groupby("fecha", as_index=False)["remesas_usd"].sum()
               .sort_values("fecha"))
    monthly["variacion_mensual_pct"] = monthly["remesas_usd"].pct_change(fill_method=None) * 100
    origins = (data.groupby("pais_origen", as_index=False)["remesas_usd"].sum()
               .nlargest(top_n, "remesas_usd"))
    provinces = (data.groupby("provincia_destino", as_index=False)["remesas_usd"].sum()
                 .nlargest(top_n, "remesas_usd"))

    start, end = monthly["fecha"].min(), monthly["fecha"].max()
    period = f"{MONTHS_ES[start.month - 1]} de {start.year} a {MONTHS_ES[end.month - 1]} de {end.year}"
    report = f"""# Informe descriptivo: remesas recibidas en Ecuador

**Fuente:** Base de Datos de Remesas de Trabajadores del Banco Central del Ecuador (BCE).

**Periodo cubierto:** {period}.

**Total registrado:** {format_usd(monthly['remesas_usd'].sum())}.

Este informe agrega registros mensuales por país de origen y provincia de destino.
Describe los datos publicados; no establece relaciones causales con migración,
pobreza, empleo u otras variables.

## Evolución mensual

{table_markdown(monthly)}

## Diez principales países de origen

{table_markdown(origins)}

## Diez principales provincias de destino

{table_markdown(provinces)}

## Gráficos

![Evolución mensual](charts/remesas_mensuales.png)

![Países de origen](charts/remesas_por_pais.png)

![Provincias de destino](charts/remesas_por_provincia.png)
"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print(f"Informe generado en {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("data/processed/bce_remesas_mensuales.csv"))
    parser.add_argument("--output", type=Path, default=Path("reports/reporte_remesas_bce.md"))
    parser.add_argument("--top-n", type=int, default=10)
    args = parser.parse_args()
    main(args.input, args.output, args.top_n)
