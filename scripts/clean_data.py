"""Convierte las observaciones WDI a una serie anual lista para análisis."""
from pathlib import Path
import argparse

import pandas as pd


def main(input_path: Path, output_path: Path) -> None:
    raw = pd.read_csv(input_path)
    raw["year"] = pd.to_numeric(raw["year"], errors="coerce")
    raw["value"] = pd.to_numeric(raw["value"], errors="coerce")
    clean = (raw.dropna(subset=["year"])
             .pivot(index="year", columns="variable", values="value")
             .reset_index()
             .sort_values("year"))
    clean["year"] = clean["year"].astype(int)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    clean.to_csv(output_path, index=False)
    print(f"Serie anual guardada en {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("data/raw/world_bank_ecuador.csv"))
    parser.add_argument("--output", type=Path, default=Path("data/processed/ecuador_migracion_remesas_anual.csv"))
    args = parser.parse_args()
    main(args.input, args.output)
