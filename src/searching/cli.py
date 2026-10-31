"""Interfaz de consola para buscar un patrón en los abstracts originales."""

import argparse
import csv
from pathlib import Path

from src.searching.service import comparar_patron
from src.similarity.corpus import cargar_corpus

RAIZ_PROYECTO = Path(__file__).resolve().parents[2]
RUTA_SALIDA_PREDETERMINADA = RAIZ_PROYECTO / "output" / "searching"


def crear_parser():
    parser = argparse.ArgumentParser(
        description="Busca coincidencias exactas con KMP, Boyer-Moore y Rabin-Karp."
    )
    parser.add_argument("--patron", help="Cadena exacta; búsqueda sensible a mayúsculas.")
    parser.add_argument(
        "--salida",
        type=Path,
        default=RUTA_SALIDA_PREDETERMINADA,
        help="Carpeta donde guardar las ocurrencias y las mediciones.",
    )
    parser.add_argument(
        "--repeticiones",
        type=int,
        default=7,
        help="Número de ejecuciones para reportar la mediana de tiempos (predeterminado: 7).",
    )
    return parser


def main(argv=None):
    parser = crear_parser()
    argumentos = parser.parse_args(argv)
    patron = argumentos.patron if argumentos.patron is not None else input("Patrón exacto: ")
    if patron == "":
        parser.error("El patrón no puede estar vacío.")

    try:
        articulos = cargar_corpus()
        resultados = comparar_patron(articulos, patron, argumentos.repeticiones)
        _guardar_ocurrencias(argumentos.salida / "ocurrencias.csv", articulos, resultados)
        _guardar_rendimiento(argumentos.salida / "rendimiento.csv", resultados)
    except (FileNotFoundError, OSError, ValueError) as error:
        parser.error(str(error))

    print(f"Búsqueda exacta (sensible a mayúsculas): {patron!r}")
    for metodo, detalle in resultados.items():
        total = sum(len(posiciones) for posiciones in detalle["ocurrencias"].values())
        print(
            f"{metodo}: {total} ocurrencias; "
            f"preprocesamiento={detalle['tiempo_preparacion_ms']:.6f} ms; "
            f"búsqueda={detalle['tiempo_busqueda_ms']:.6f} ms; "
            f"repeticiones={detalle['repeticiones']}; "
            f"comparaciones={detalle['comparaciones']}; "
            f"colisiones={detalle['colisiones']}"
        )
    print(f"Resultados guardados en: {argumentos.salida}")


def _guardar_ocurrencias(ruta, articulos, resultados):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", encoding="utf-8-sig", newline="") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["algoritmo", "id_articulo", "titulo", "cantidad", "posiciones_1_based"])
        for metodo, detalle in resultados.items():
            for identificador, posiciones in detalle["ocurrencias"].items():
                escritor.writerow([
                    metodo,
                    identificador,
                    articulos[identificador]["titulo"],
                    len(posiciones),
                    ";".join(str(posicion + 1) for posicion in posiciones),
                ])


def _guardar_rendimiento(ruta, resultados):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", encoding="utf-8-sig", newline="") as archivo:
        campos = [
            "algoritmo",
            "tiempo_preparacion_ms",
            "tiempo_busqueda_ms",
            "repeticiones",
            "comparaciones_caracteres",
            "colisiones_hash",
        ]
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        for metodo, detalle in resultados.items():
            escritor.writerow({
                "algoritmo": metodo,
                "tiempo_preparacion_ms": f"{detalle['tiempo_preparacion_ms']:.9f}",
                "tiempo_busqueda_ms": f"{detalle['tiempo_busqueda_ms']:.9f}",
                "repeticiones": detalle["repeticiones"],
                "comparaciones_caracteres": detalle["comparaciones"],
                "colisiones_hash": detalle["colisiones"],
            })


if __name__ == "__main__":
    main()
