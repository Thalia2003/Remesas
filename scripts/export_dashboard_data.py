"""Exporta los datos procesados a JSON para el dashboard interactivo."""
from pathlib import Path
import json
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = ROOT_DIR / "data" / "processed"
OUTPUT_JSON = ROOT_DIR / "data" / "dashboard_data.json"


def export_data() -> None:
    annual_csv = PROCESSED_DIR / "indicadores_anuales.csv"
    bce_csv = PROCESSED_DIR / "bce_remesas_mensuales.csv"
    diaspora_csv = PROCESSED_DIR / "ecuador_diaspora_un.csv"

    annual_df = pd.read_csv(annual_csv)
    bce_df = pd.read_csv(bce_csv)
    diaspora_df = pd.read_csv(diaspora_csv) if diaspora_csv.exists() else pd.DataFrame()

    # Filtrar desde 1990 para series anuales
    annual_filtered = annual_df[annual_df["year"] >= 1990].fillna(0)

    # Agrupar BCE por fecha
    bce_monthly = bce_df.groupby("fecha", as_index=False)["remesas_usd"].sum().sort_values("fecha")

    # Top Países
    bce_countries = (
        bce_df.groupby("pais_origen", as_index=False)["remesas_usd"]
        .sum()
        .nlargest(10, "remesas_usd")
        .sort_values("remesas_usd", ascending=False)
    )

    # Top Provincias
    bce_provinces = (
        bce_df.groupby("provincia_destino", as_index=False)["remesas_usd"]
        .sum()
        .nlargest(10, "remesas_usd")
        .sort_values("remesas_usd", ascending=False)
    )

    data = {
        "annual": {
            "years": annual_filtered["year"].tolist(),
            "remesas_usd": (annual_filtered["remesas_recibidas_usd"] / 1e9).round(3).tolist(),
            "pct_pib": annual_filtered["remesas_pct_pib"].round(2).tolist(),
            "pib_usd": (annual_filtered["pib_usd"] / 1e9).round(2).tolist(),
        },
        "bce_monthly": {
            "dates": bce_monthly["fecha"].tolist(),
            "remesas_millones": (bce_monthly["remesas_usd"] / 1e6).round(2).tolist(),
        },
        "top_countries": {
            "countries": bce_countries["pais_origen"].tolist(),
            "remesas_millones": (bce_countries["remesas_usd"] / 1e6).round(2).tolist(),
        },
        "top_provinces": {
            "provinces": bce_provinces["provincia_destino"].tolist(),
            "remesas_millones": (bce_provinces["remesas_usd"] / 1e6).round(2).tolist(),
        },
        "diaspora": {
            "years": diaspora_df["year"].tolist() if not diaspora_df.empty else [],
            "stock_miles": (diaspora_df["ecuatorianos_residentes_exterior"] / 1e3).round(1).tolist() if not diaspora_df.empty else [],
        },
    }

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Datos exportados a {OUTPUT_JSON}")


if __name__ == "__main__":
    export_data()
