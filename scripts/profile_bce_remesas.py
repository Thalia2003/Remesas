"""Muestra el esquema de la base BCE sin modificar el archivo original."""
from pathlib import Path
import argparse

import pandas as pd


def read_csv_flexible(path: Path, nrows: int | None = 5) -> pd.DataFrame:
    for encoding in ("utf-8-sig", "latin-1"):
        for delimiter in ("|", ",", ";"):
            try:
                frame = pd.read_csv(path, encoding=encoding, sep=delimiter, nrows=nrows)
                if len(frame.columns) > 1:
                    return frame
            except UnicodeDecodeError:
                continue
    raise ValueError("No fue posible identificar codificación y separador del CSV BCE")


def main(input_path: Path) -> None:
    sample = read_csv_flexible(input_path)
    print("Columnas disponibles:")
    for column in sample.columns:
        print(f"- {column}")
    print("\nMuestra:")
    print(sample.to_string(index=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("data/raw/bce_remesas_trabajadores.csv"))
    args = parser.parse_args()
    main(args.input)
