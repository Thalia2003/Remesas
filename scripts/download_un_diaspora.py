"""Descarga la tabla oficial de Naciones Unidas por país de origen."""
from pathlib import Path
import argparse

import requests

URL = (
    "https://www.un.org/development/desa/pd/sites/www.un.org.development.desa.pd/files/"
    "undesa_pd_2024_ims_stock_by_sex_and_origin.xlsx"
)


def main(output: Path) -> None:
    response = requests.get(
        URL,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://www.un.org/development/desa/pd/content/international-migrant-stock",
        },
        timeout=90,
    )
    response.raise_for_status()
    if not response.content.startswith(b"PK"):
        raise ValueError("La respuesta no parece un archivo XLSX")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(response.content)
    print(f"Archivo de Naciones Unidas descargado en {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("data/raw/un_migrant_stock_by_origin.xlsx"))
    main(parser.parse_args().output)
