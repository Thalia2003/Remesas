"""Extrae el stock de personas nacidas en Ecuador residentes en el exterior.

Requiere el archivo 'International Migrant Stock 2024 - Total, origin' descargado
desde el portal de Naciones Unidas. Se declaran los metadatos de la hoja para no
asumir una estructura fija de Excel.
"""
from pathlib import Path
import argparse

import pandas as pd


def main(input_path: Path, output_path: Path, sheet_name: str | int,
         header_row: int, origin_column: str, origin_name: str) -> None:
    frame = pd.read_excel(input_path, sheet_name=sheet_name, header=header_row)
    if origin_column not in frame.columns:
        raise ValueError(f"No se encontró la columna de origen {origin_column!r}")
    selected = frame.loc[
        frame[origin_column].astype("string").str.strip().str.upper().eq(origin_name.strip().upper())
    ].copy()
    if selected.empty:
        raise ValueError(f"No se encontró {origin_name!r}; revise columna y nombre de origen")

    year_columns = [column for column in frame.columns if str(column).isdigit() and 1990 <= int(column) <= 2024]
    if not year_columns:
        raise ValueError("No se identificaron columnas anuales entre 1990 y 2024")
    values = selected[year_columns].apply(pd.to_numeric, errors="coerce").sum(axis=0)
    result = pd.DataFrame({
        "year": [int(column) for column in values.index],
        "ecuatorianos_residentes_exterior": values.values,
        "source": "un_desa_international_migrant_stock_2024",
    }).sort_values("year")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output_path, index=False)
    print(f"Serie de diáspora guardada en {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("data/processed/ecuador_diaspora_un.csv"))
    parser.add_argument("--sheet-name", default=0)
    parser.add_argument("--header-row", type=int, default=0)
    parser.add_argument("--origin-column", required=True)
    parser.add_argument("--origin-name", default="Ecuador")
    args = parser.parse_args()
    sheet = int(args.sheet_name) if str(args.sheet_name).isdigit() else args.sheet_name
    main(args.input, args.output, sheet, args.header_row, args.origin_column, args.origin_name)
