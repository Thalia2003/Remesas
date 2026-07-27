import importlib.util
from pathlib import Path

import pandas as pd


def test_indicator_script_creates_growth_columns(tmp_path):
    input_path = tmp_path / "series.csv"
    output_path = tmp_path / "indicators.csv"
    pd.DataFrame({
        "year": [2022, 2023],
        "remesas_recibidas_usd": [1_000_000_000, 1_100_000_000],
        "pib_usd": [100_000_000_000, 105_000_000_000],
    }).to_csv(input_path, index=False)
    spec = importlib.util.spec_from_file_location("calculate_indicators", Path("scripts/calculate_indicators.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.main(input_path, output_path)
    result = pd.read_csv(output_path)
    assert round(result.loc[1, "crecimiento_remesas_pct"], 6) == 10
    assert "remesas_miles_de_millones_usd" in result.columns
