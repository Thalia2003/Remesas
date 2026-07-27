"""Orquestador principal del proyecto Migración y Remesas en Ecuador.

Permite ejecutar el flujo completo o fases específicas desde la línea de comandos.
"""
from pathlib import Path
import argparse
import sys
import subprocess

# Asegurar que el directorio de scripts esté en el PYTHONPATH
ROOT_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = ROOT_DIR / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))


def run_annual_pipeline() -> None:
    print("=== [1/4] Ejecutando Pipeline Anual (Banco Mundial + UN) ===")
    import download_data
    import clean_data
    import validate_data
    import calculate_indicators
    import download_un_diaspora
    import import_un_diaspora

    raw_wb = ROOT_DIR / "data" / "raw" / "world_bank_ecuador.csv"
    processed_annual = ROOT_DIR / "data" / "processed" / "ecuador_migracion_remesas_anual.csv"
    indicators_csv = ROOT_DIR / "data" / "processed" / "indicadores_anuales.csv"
    diaspora_raw = ROOT_DIR / "data" / "raw" / "un_migrant_stock_by_origin.xlsx"
    diaspora_csv = ROOT_DIR / "data" / "processed" / "ecuador_diaspora_un.csv"

    download_data.main(raw_wb)
    clean_data.main(raw_wb, processed_annual)

    import pandas as pd
    frame = pd.read_csv(processed_annual)
    errors = validate_data.validate(frame)
    if errors:
        print(f"Advertencias en validación: {errors}")
    else:
        print("Validación de datos anuales exitosa.")

    calculate_indicators.main(processed_annual, indicators_csv)

    if not diaspora_raw.exists():
        download_un_diaspora.main(diaspora_raw)
    if diaspora_raw.exists():
        import_un_diaspora.main(
            input_path=diaspora_raw,
            output_path=diaspora_csv,
            sheet_name="Table 1",
            header_row=10,
            origin_column="Region, development group, country or area",
            origin_name="Ecuador",
        )


def run_bce_pipeline() -> None:
    print("=== [2/4] Ejecutando Pipeline Mensual (Banco Central del Ecuador) ===")
    import download_bce_remesas
    import profile_bce_remesas
    import clean_bce_remesas

    raw_bce = ROOT_DIR / "data" / "raw" / "bce_remesas_trabajadores.csv"
    processed_bce = ROOT_DIR / "data" / "processed" / "bce_remesas_mensuales.csv"

    if not raw_bce.exists():
        download_bce_remesas.main(raw_bce)

    profile_bce_remesas.main(raw_bce)
    clean_bce_remesas.main(
        input_path=raw_bce,
        output_path=processed_bce,
        year_column="anio",
        month_column="mes",
        amount_column="monto_USD",
        operation_column="descr_tipo_transaccion",
        received_value="RECIBIDAS",
        origin_column="descr_pais",
        province_column="descr_provincia",
    )


def run_reports_and_charts() -> None:
    print("=== [3/4] Generando Gráficos y Diagnósticos ===")
    import econometric_model
    import generate_charts
    import generate_report
    import export_dashboard_data
    import generate_doc_and_pdf

    processed_annual = ROOT_DIR / "data" / "processed" / "ecuador_migracion_remesas_anual.csv"
    diaspora_csv = ROOT_DIR / "data" / "processed" / "ecuador_diaspora_un.csv"
    diag_md = ROOT_DIR / "reports" / "diagnostico_anual.md"
    bce_csv = ROOT_DIR / "data" / "processed" / "bce_remesas_mensuales.csv"
    charts_dir = ROOT_DIR / "reports" / "charts"
    bce_report = ROOT_DIR / "reports" / "reporte_remesas_bce.md"

    econometric_model.main(processed_annual, diaspora_csv, diag_md)
    generate_charts.main(bce_csv, charts_dir)
    generate_report.main(bce_csv, bce_report)
    export_dashboard_data.export_data()
    generate_doc_and_pdf.build_docx()
    generate_doc_and_pdf.build_pdf()


def run_tests() -> None:
    print("=== [4/4] Ejecutando Suite de Pruebas Unitarias ===")
    result = subprocess.run([sys.executable, "-m", "pytest"], cwd=ROOT_DIR)
    if result.returncode != 0:
        raise RuntimeError("La suite de pruebas falló.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Orquestador del análisis de migración y remesas en Ecuador")
    parser.add_argument(
        "action",
        nargs="?",
        default="run-all",
        choices=["run-all", "annual", "bce", "reports", "test"],
        help="Acción a ejecutar: run-all (defecto), annual, bce, reports, test",
    )
    args = parser.parse_args()

    if args.action == "run-all":
        run_annual_pipeline()
        run_bce_pipeline()
        run_reports_and_charts()
        run_tests()
        print("\n[OK] Proceso completado exitosamente con todas las validaciones.")
    elif args.action == "annual":
        run_annual_pipeline()
    elif args.action == "bce":
        run_bce_pipeline()
    elif args.action == "reports":
        run_reports_and_charts()
    elif args.action == "test":
        run_tests()


if __name__ == "__main__":
    main()
