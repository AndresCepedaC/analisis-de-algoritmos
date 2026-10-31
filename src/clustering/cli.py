"""Interfaz de consola para generar clustering, métricas y dendrogramas."""

import argparse
import csv
from pathlib import Path

from src.clustering.hierarchical import METODOS, cortar_arbol
from src.clustering.service import evaluar_enlaces, matriz_distancias_tfidf
from src.clustering.visualization import guardar_dendrograma
from src.similarity.corpus import cargar_corpus

RAIZ_PROYECTO = Path(__file__).resolve().parents[2]
RUTA_SALIDA_PREDETERMINADA = RAIZ_PROYECTO / "output" / "clustering"


def crear_parser():
    parser = argparse.ArgumentParser(
        description="Agrupa los abstracts con tres enlaces jerárquicos desde cero."
    )
    parser.add_argument(
        "--salida",
        type=Path,
        default=RUTA_SALIDA_PREDETERMINADA,
        help="Carpeta donde guardar dendrogramas y CSV de resultados.",
    )
    return parser


def main(argv=None):
    parser = crear_parser()
    argumentos = parser.parse_args(argv)
    try:
        articulos = cargar_corpus()
        ids, matriz_distancias = matriz_distancias_tfidf(articulos)
        resultados = evaluar_enlaces(matriz_distancias)
        _guardar_matriz(argumentos.salida / "distancias_coseno.csv", ids, matriz_distancias)
        _guardar_puntuaciones(argumentos.salida / "silhouette.csv", resultados)
        _guardar_agrupaciones(
            argumentos.salida / "agrupaciones_mejores.csv",
            articulos,
            ids,
            resultados,
        )

        for metodo in METODOS:
            detalle = resultados[metodo]
            guardar_dendrograma(
                articulos,
                ids,
                detalle["fusiones"],
                metodo,
                argumentos.salida / f"dendrograma_{metodo}.png",
            )
            _guardar_fusiones(
                argumentos.salida / f"fusiones_{metodo}.csv",
                detalle["fusiones"],
            )
    except (FileNotFoundError, OSError, ValueError) as error:
        parser.error(str(error))

    print(f"Abstracts agrupados: {len(ids)}")
    for metodo in METODOS:
        detalle = resultados[metodo]
        print(
            f"{metodo.title()} linkage: k={detalle['mejor_k']}, "
            f"silhouette={detalle['mejor_silhouette']:.6f}"
        )
    mayor_silhouette = max(
        resultados[metodo]["mejor_silhouette"] for metodo in METODOS
    )
    mejores_metodos = [
        metodo
        for metodo in METODOS
        if abs(resultados[metodo]["mejor_silhouette"] - mayor_silhouette) < 1e-12
    ]
    if len(mejores_metodos) == 1:
        print(f"Mayor silhouette: {mejores_metodos[0].title()} linkage")
    else:
        nombres = ", ".join(metodo.title() for metodo in mejores_metodos)
        print(f"Empate en mayor silhouette entre: {nombres}")
    print(f"Archivos guardados en: {argumentos.salida}")


def _guardar_matriz(ruta, ids, matriz):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", encoding="utf-8-sig", newline="") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["id", *ids])
        for identificador, fila in zip(ids, matriz):
            escritor.writerow([identificador, *[f"{valor:.12f}" for valor in fila]])


def _guardar_puntuaciones(ruta, resultados):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", encoding="utf-8-sig", newline="") as archivo:
        campos = ["metodo", "k", "silhouette", "seleccionado"]
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        for metodo, detalle in resultados.items():
            for cantidad_grupos, puntuacion in detalle["puntuaciones"]:
                escritor.writerow({
                    "metodo": metodo,
                    "k": cantidad_grupos,
                    "silhouette": f"{puntuacion:.12f}",
                    "seleccionado": cantidad_grupos == detalle["mejor_k"],
                })


def _guardar_fusiones(ruta, fusiones):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", encoding="utf-8-sig", newline="") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["paso", "nodo_izquierdo", "nodo_derecho", "distancia", "tamano"])
        for paso, fusion in enumerate(fusiones, start=1):
            escritor.writerow([
                paso,
                fusion.left,
                fusion.right,
                f"{fusion.distance:.12f}",
                fusion.size,
            ])


def _guardar_agrupaciones(ruta, articulos, ids, resultados):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", encoding="utf-8-sig", newline="") as archivo:
        campos = ["id", "titulo"] + [f"{metodo}_grupo" for metodo in METODOS]
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()

        etiquetas_por_metodo = {}
        for metodo, detalle in resultados.items():
            etiquetas_por_metodo[metodo] = cortar_arbol(
                len(ids), detalle["fusiones"], detalle["mejor_k"]
            )

        for indice, identificador in enumerate(ids):
            fila = {
                "id": identificador,
                "titulo": articulos[identificador]["titulo"],
            }
            for metodo in METODOS:
                fila[f"{metodo}_grupo"] = etiquetas_por_metodo[metodo][indice] + 1
            escritor.writerow(fila)


if __name__ == "__main__":
    main()
