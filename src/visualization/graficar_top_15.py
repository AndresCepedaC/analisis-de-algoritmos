
"""
Genera una gráfica de las 15 palabras más frecuentes
obtenidas mediante los tres algoritmos de ordenamiento.
"""

import csv
from pathlib import Path

import matplotlib.pyplot as plt


RUTA_CSV = Path("data/top_15_algoritmos.csv")
RUTA_GRAFICA = Path("data/top_15_palabras.png")


def cargar_top_15():
    """Lee los resultados de los tres algoritmos."""

    resultados = {}

    with open(RUTA_CSV, "r", encoding="utf-8", newline="") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            algoritmo = fila["algoritmo"]

            if algoritmo not in resultados:
                resultados[algoritmo] = []

            resultados[algoritmo].append(
                (fila["palabra"], int(fila["frecuencia"]))
            )
    return resultados

def graficar_top_15():
    resultados = cargar_top_15()
    # Usamos Counting Sort como referencia.
    datos = resultados["Counting Sort"]
    palabras = [palabra for palabra, _ in datos]
    frecuencias = [frecuencia for _, frecuencia in datos]

    # Verificamos que los tres algoritmos coincidan.
    coinciden = all(
        resultados[nombre] == datos
        for nombre in resultados
    )

    if not coinciden:
        raise ValueError(
            "Los resultados de los algoritmos no coinciden."
        )

    plt.figure(figsize=(12, 6))
    plt.bar(palabras, frecuencias)

    plt.title("15 palabras más frecuentes en los abstracts")
    plt.xlabel("Palabras")
    plt.ylabel("Frecuencia")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    RUTA_GRAFICA.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(RUTA_GRAFICA, dpi=300, bbox_inches="tight")
    plt.show()

    print(f"Gráfica guardada en: {RUTA_GRAFICA}")


if __name__ == "__main__":
    graficar_top_15()
