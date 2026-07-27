"""Genera gráficos descriptivos a partir de las remesas mensuales del BCE."""
from pathlib import Path
import argparse

import matplotlib.pyplot as plt
import pandas as pd

BLUE = "#075985"
ORANGE = "#c2410c"


def save_bar(frame: pd.DataFrame, label: str, title: str, output: Path, color: str) -> None:
    data = frame.groupby(label, as_index=False)["remesas_usd"].sum().nlargest(10, "remesas_usd")
    data = data.sort_values("remesas_usd")
    fig, axis = plt.subplots(figsize=(10, 6))
    axis.barh(data[label], data["remesas_usd"] / 1_000_000, color=color)
    axis.set_title(title, loc="left", fontweight="bold")
    axis.set_xlabel("Millones de USD")
    axis.grid(axis="x", alpha=0.2)
    fig.tight_layout()
    fig.savefig(output, dpi=160)
    plt.close(fig)


def main(input_path: Path, output_dir: Path) -> None:
    data = pd.read_csv(input_path, parse_dates=["fecha"])
    output_dir.mkdir(parents=True, exist_ok=True)

    monthly = data.groupby("fecha", as_index=False)["remesas_usd"].sum().sort_values("fecha")
    fig, axis = plt.subplots(figsize=(10, 5))
    axis.plot(monthly["fecha"], monthly["remesas_usd"] / 1_000_000, marker="o", color=BLUE, linewidth=2)
    axis.set_title("Remesas recibidas por mes", loc="left", fontweight="bold")
    axis.set_ylabel("Millones de USD")
    axis.set_xlabel("")
    axis.grid(alpha=0.2)
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(output_dir / "remesas_mensuales.png", dpi=160)
    plt.close(fig)

    save_bar(data, "pais_origen", "Principales países de origen de remesas", output_dir / "remesas_por_pais.png", BLUE)
    save_bar(data, "provincia_destino", "Principales provincias de destino", output_dir / "remesas_por_provincia.png", ORANGE)
    print(f"Gráficos generados en {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("data/processed/bce_remesas_mensuales.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("reports/charts"))
    args = parser.parse_args()
    main(args.input, args.output_dir)
