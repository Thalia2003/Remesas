"""Descarga indicadores WDI de Ecuador y conserva la respuesta tabular cruda."""
from __future__ import annotations

from pathlib import Path
import argparse

import pandas as pd
import requests

INDICATORS = {
    "BX.TRF.PWKR.CD.DT": "remesas_recibidas_usd",
    "BX.TRF.PWKR.DT.GD.ZS": "remesas_pct_pib",
    "SM.POP.TOTL": "stock_migrantes_internacionales",
    "NY.GDP.MKTP.CD": "pib_usd",
}
BASE_URL = "https://api.worldbank.org/v2/country/ECU/indicator/{indicator}"


def fetch_indicator(indicator: str) -> list[dict]:
    response = requests.get(
        BASE_URL.format(indicator=indicator),
        params={"format": "json", "per_page": 1000}, timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, list) or len(payload) < 2:
        raise ValueError(f"Respuesta inesperada de WDI para {indicator}")
    return payload[1] or []


def main(output: Path) -> None:
    rows = []
    for code, variable in INDICATORS.items():
        for record in fetch_indicator(code):
            rows.append({
                "source": "world_bank_wdi",
                "country_code": "ECU",
                "indicator_code": code,
                "variable": variable,
                "year": record["date"],
                "value": record["value"],
            })
    output.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(output, index=False)
    print(f"Descargadas {len(rows)} observaciones en {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("data/raw/world_bank_ecuador.csv"))
    main(parser.parse_args().output)
