import importlib.util
from pathlib import Path

import pandas as pd


def load_module(name: str):
    path = Path("scripts") / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_diagnostic_report_and_chart_are_generated(tmp_path):
    model = load_module("econometric_model")

    input_path = tmp_path / "ecuador_migracion_remesas_anual.csv"
    diaspora_path = tmp_path / "ecuador_diaspora_un.csv"
    output_path = tmp_path / "diagnostico_anual.md"

    pd.DataFrame({
        "year": [2018, 2019, 2020],
        "remesas_recibidas_usd": [3_200_000_000, 3_500_000_000, 3_800_000_000],
        "remesas_pct_pib": [3.0, 3.1, 3.2],
        "pib_usd": [100_000_000_000, 102_000_000_000, 98_000_000_000],
    }).to_csv(input_path, index=False)

    pd.DataFrame({
        "year": [2018, 2019, 2020],
        "ecuatorianos_residentes_exterior": [1_000_000, 1_050_000, 1_100_000],
    }).to_csv(diaspora_path, index=False)

    model.main(input_path, diaspora_path, output_path)

    report = output_path.read_text(encoding="utf-8")
    chart_path = output_path.parent / "charts" / "remesas_vs_diaspora.png"

    assert output_path.exists()
    assert chart_path.exists()
    assert "Remesas y diáspora ecuatoriana" in report
    assert "no identifica una relación causal" in report


def test_export_dashboard_data_generates_json():
    exporter = load_module("export_dashboard_data")
    json_file = Path("data/dashboard_data.json")
    exporter.export_data()
    assert json_file.exists()

