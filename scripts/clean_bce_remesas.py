"""Normaliza la base mensual de remesas de trabajadores publicada por el BCE."""
from pathlib import Path
import argparse

import pandas as pd

import sys

sys_dir = str(Path(__file__).resolve().parent)
if sys_dir not in sys.path:
    sys.path.insert(0, sys_dir)

try:
    from profile_bce_remesas import read_csv_flexible
except ModuleNotFoundError:
    from scripts.profile_bce_remesas import read_csv_flexible


def parse_amount(series: pd.Series) -> pd.Series:
    text = series.astype(str).str.strip().str.replace("$", "", regex=False)
    # Si hay coma y punto, se elimina el separador de miles.
    text = text.str.replace(r"(?<=\d)[,.](?=\d{3}(?:\D|$))", "", regex=True)
    text = text.str.replace(",", ".", regex=False)
    return pd.to_numeric(text, errors="coerce")


def main(input_path: Path, output_path: Path, year_column: str, month_column: str,
         amount_column: str, operation_column: str, received_value: str,
         origin_column: str | None, province_column: str | None) -> None:
    frame = read_csv_flexible(input_path, nrows=None)
    requested = [year_column, month_column, amount_column, operation_column,
                 origin_column, province_column]
    missing = [column for column in requested if column and column not in frame.columns]
    if missing:
        raise ValueError(f"Columnas no encontradas: {', '.join(missing)}")

    operations = frame[operation_column].astype("string").str.strip().str.upper()
    selected = frame.loc[operations.eq(received_value.strip().upper())].copy()
    if selected.empty:
        raise ValueError(f"No hay registros con {operation_column}={received_value!r}")

    result = pd.DataFrame({
        "fecha": pd.to_datetime({
            "year": pd.to_numeric(selected[year_column], errors="coerce"),
            "month": pd.to_numeric(selected[month_column], errors="coerce"),
            "day": 1,
        }, errors="coerce"),
        "remesas_usd": parse_amount(selected[amount_column]),
    })
    if origin_column:
        result["pais_origen"] = selected[origin_column].astype("string").str.strip()
    if province_column:
        result["provincia_destino"] = selected[province_column].astype("string").str.strip()
    result = result.dropna(subset=["fecha", "remesas_usd"])
    if result["remesas_usd"].lt(0).any():
        raise ValueError("La columna de monto contiene valores negativos")
    dimensions = ["fecha"]
    if origin_column:
        dimensions.append("pais_origen")
    if province_column:
        dimensions.append("provincia_destino")
    result = result.groupby(dimensions, dropna=False, as_index=False)["remesas_usd"].sum()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output_path, index=False)
    print(f"Guardadas {len(result)} observaciones normalizadas en {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("data/raw/bce_remesas_trabajadores.csv"))
    parser.add_argument("--output", type=Path, default=Path("data/processed/bce_remesas_mensuales.csv"))
    parser.add_argument("--year-column", default="anio")
    parser.add_argument("--month-column", default="mes")
    parser.add_argument("--amount-column", default="monto_USD")
    parser.add_argument("--operation-column", default="descr_tipo_transaccion")
    parser.add_argument("--received-value", default="RECIBIDAS")
    parser.add_argument("--origin-column", default="descr_pais")
    parser.add_argument("--province-column", default="descr_provincia")
    args = parser.parse_args()
    main(args.input, args.output, args.year_column, args.month_column,
         args.amount_column, args.operation_column, args.received_value,
         args.origin_column, args.province_column)
