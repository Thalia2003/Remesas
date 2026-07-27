"""Descarga la base mensual de remesas de trabajadores publicada por el BCE."""
from pathlib import Path
import argparse

import requests

URL = (
    "https://contenido.bce.fin.ec/documentos/Estadisticas/SectorExterno/"
    "BalanzaPagos/Remesas/BDD_Remesas_de_trabajadores.csv"
)


def main(output: Path) -> None:
    response = requests.get(URL, timeout=60)
    response.raise_for_status()
    if not response.content:
        raise ValueError("El BCE respondió sin contenido")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(response.content)
    print(f"Base BCE descargada en {output} ({len(response.content)} bytes)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("data/raw/bce_remesas_trabajadores.csv"))
    main(parser.parse_args().output)
