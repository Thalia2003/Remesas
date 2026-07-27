import importlib.util
from pathlib import Path

import pandas as pd


def load_module(name: str):
    path = Path("scripts") / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_validation_accepts_valid_series():
    validate_data = load_module("validate_data")
    frame = pd.DataFrame({
        "year": [2022, 2023],
        "remesas_recibidas_usd": [4_000_000_000, 4_500_000_000],
        "remesas_pct_pib": [3.5, 3.8],
        "pib_usd": [110_000_000_000, 115_000_000_000],
    })
    assert validate_data.validate(frame) == []


def test_validation_rejects_negative_remittances():
    validate_data = load_module("validate_data")
    frame = pd.DataFrame({
        "year": [2022], "remesas_recibidas_usd": [-1],
        "remesas_pct_pib": [1], "pib_usd": [1],
    })
    assert "Hay remesas recibidas negativas" in validate_data.validate(frame)


def test_bce_amount_parser_handles_spanish_and_english_formats():
    bce_cleaner = load_module("clean_bce_remesas")
    values = pd.Series(["1,234.56", "1.234,56", "$ 50"])
    assert bce_cleaner.parse_amount(values).tolist() == [1234.56, 1234.56, 50.0]
