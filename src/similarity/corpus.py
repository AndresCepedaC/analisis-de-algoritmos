"""Carga y valida el catálogo de abstracts preparado para el proyecto."""

import csv
from pathlib import Path

RAIZ_PROYECTO = Path(__file__).resolve().parents[2]
RUTA_CORPUS = RAIZ_PROYECTO / "data" / "corpus_articulos.csv"


def cargar_corpus(ruta=RUTA_CORPUS):
    """Devuelve artículos indexados por identificador numérico."""
    ruta = Path(ruta)
    if not ruta.is_file():
        raise FileNotFoundError(
            f"No existe {ruta}. Genéralo con "
            "python -m src.extraction.construir_corpus."
        )

    with ruta.open("r", encoding="utf-8-sig", newline="") as archivo:
        filas = csv.DictReader(archivo)
        requeridos = {"id", "titulo", "autores", "abstract", "abstract_normalizado"}
        faltantes = requeridos - set(filas.fieldnames or [])
        if faltantes:
            raise ValueError(f"Al catálogo le faltan columnas: {sorted(faltantes)}")

        articulos = {}
        for fila in filas:
            identificador = int(fila["id"])
            if identificador in articulos:
                raise ValueError(f"El identificador {identificador} está repetido.")
            if not fila["abstract_normalizado"].strip():
                raise ValueError(f"El artículo {identificador} no tiene abstract normalizado.")
            articulos[identificador] = fila

    if len(articulos) < 2:
        raise ValueError("El catálogo debe contener al menos dos artículos.")
    return articulos
