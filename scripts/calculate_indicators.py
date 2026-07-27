"""Calcula indicadores descriptivos sin inferir causalidad."""
from pathlib import Path
import argparse

import pandas as pd


def main(input_path: Path, output_path: Path) -> None:
    frame = pd.read_csv(input_path).sort_values("year").copy()
    frame["remesas_miles_de_millones_usd"] = frame["remesas_recibidas_usd"] / 1_000_000_000
    frame["crecimiento_remesas_pct"] = frame["remesas_recibidas_usd"].pct_change(fill_method=None) * 100
    frame["crecimiento_pib_pct"] = frame["pib_usd"].pct_change(fill_method=None) * 100
    output_path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(output_path, index=False)
    print(f"Indicadores guardados en {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("data/processed/ecuador_migracion_remesas_anual.csv"))
    parser.add_argument("--output", type=Path, default=Path("data/processed/indicadores_anuales.csv"))
    args = parser.parse_args()
    main(args.input, args.output)
