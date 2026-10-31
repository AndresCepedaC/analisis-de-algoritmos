"""Punto de entrada de la aplicación del proyecto."""

import sys

from src.similarity.cli import main as ejecutar_similitud


if __name__ == "__main__":
    argumentos = sys.argv[1:]
    if argumentos and argumentos[0] == "clustering":
        from src.clustering.cli import main as ejecutar_clustering

        ejecutar_clustering(argumentos[1:])
    elif argumentos and argumentos[0] == "busqueda":
        from src.searching.cli import main as ejecutar_busqueda

        ejecutar_busqueda(argumentos[1:])
    else:
        ejecutar_similitud(argumentos)
