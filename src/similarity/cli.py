"""Interfaz de consola para comparar abstracts del corpus."""

import argparse
import csv
from pathlib import Path

from src.similarity.corpus import cargar_corpus
from src.similarity.embeddings import cargar_fasttext, cargar_glove
from src.similarity.service import comparar_articulos


def crear_parser():
    parser = argparse.ArgumentParser(
        description="Compara abstracts con cuatro algoritmos clásicos y dos embeddings."
    )
    parser.add_argument("--ids", nargs="+", type=int, required=True, help="IDs de dos o más artículos")
    parser.add_argument("--glove", type=Path, help="Ruta a vectores GloVe de texto")
    parser.add_argument("--fasttext", type=Path, help="Ruta a vectores FastText de texto (.vec)")
    parser.add_argument("--salida", type=Path, help="Ruta opcional para exportar resultados CSV")
    return parser


def main(argv=None):
    parser = crear_parser()
    argumentos = parser.parse_args(argv)

    try:
        articulos = cargar_corpus()
        vocabulario = {
            token
            for articulo in articulos.values()
            for token in articulo["abstract_normalizado"].split()
        }
        if argumentos.glove:
            print("Cargando vectores GloVe...", flush=True)
        glove = (
            cargar_glove(argumentos.glove, vocabulario)
            if argumentos.glove
            else None
        )
        if argumentos.fasttext:
            print("Cargando vectores FastText...", flush=True)
        fasttext = (
            cargar_fasttext(argumentos.fasttext, vocabulario)
            if argumentos.fasttext
            else None
        )
        resultados = comparar_articulos(
            articulos, argumentos.ids, glove=glove, fasttext=fasttext
        )
    except (FileNotFoundError, OSError, ValueError, RuntimeError) as error:
        parser.error(str(error))

    print("Comparación de similitud textual")
    for resultado in resultados:
        articulo_a = articulos[resultado["id_a"]]
        articulo_b = articulos[resultado["id_b"]]
        print(f"\nArtículo {resultado['id_a']}: {articulo_a['titulo']}")
        print(f"Artículo {resultado['id_b']}: {articulo_b['titulo']}")
        for nombre, valor in resultado["medidas"].items():
            texto_valor = "sin vocabulario común" if valor is None else f"{valor:.6f}"
            print(f"  {nombre}: {texto_valor}")
        for nombre, cobertura in resultado["coberturas"].items():
            print(f"  {nombre}: {cobertura} tokens")

    if argumentos.salida:
        _guardar_csv(argumentos.salida, resultados)
        print(f"\nResultados guardados en: {argumentos.salida}")
    elif not argumentos.glove or not argumentos.fasttext:
        print("\nPara ejecutar los dos métodos con embeddings, indica --glove y --fasttext.")


def _guardar_csv(ruta, resultados):
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    nombres_medidas = list(resultados[0]["medidas"])
    nombres_cobertura = list(resultados[0]["coberturas"])
    with ruta.open("w", encoding="utf-8-sig", newline="") as archivo:
        escritor = csv.DictWriter(
            archivo,
            fieldnames=["id_a", "id_b", *nombres_medidas, *nombres_cobertura],
        )
        escritor.writeheader()
        for resultado in resultados:
            escritor.writerow({
                "id_a": resultado["id_a"],
                "id_b": resultado["id_b"],
                **resultado["medidas"],
                **resultado["coberturas"],
            })


if __name__ == "__main__":
    main()
