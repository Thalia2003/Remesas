"""Validaciones mínimas para la serie anual de migración y remesas."""
from pathlib import Path
import argparse
import sys

import pandas as pd

REQUIRED = {"year", "remesas_recibidas_usd", "remesas_pct_pib", "pib_usd"}


def validate(frame: pd.DataFrame) -> list[str]:
    errors = []
    missing = REQUIRED - set(frame.columns)
    if missing:
        errors.append(f"Faltan columnas requeridas: {', '.join(sorted(missing))}")
        return errors
    if frame["year"].duplicated().any():
        errors.append("Hay años duplicados")
    if not frame["year"].is_monotonic_increasing:
        errors.append("Los años no están ordenados ascendentemente")
    if frame["remesas_recibidas_usd"].dropna().lt(0).any():
        errors.append("Hay remesas recibidas negativas")
    if frame["remesas_recibidas_usd"].notna().sum() == 0:
        errors.append("No hay observaciones de remesas")
    return errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("data/processed/ecuador_migracion_remesas_anual.csv"))
    args = parser.parse_args()
    errors = validate(pd.read_csv(args.input))
    if errors:
        print("VALIDACIÓN FALLIDA:\n- " + "\n- ".join(errors))
        sys.exit(1)
    print("Validación aprobada")
