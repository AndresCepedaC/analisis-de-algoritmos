
"""
Compara Counting Sort, Radix Sort y Bucket Sort
usando las mismas frecuencias y varias mediciones.
"""

import csv
import sys
import time
from pathlib import Path
from statistics import median

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.sorting.counting_sort import counting_sort
from src.sorting.radix_sort import radix_sort
from src.sorting.bucket_sort import bucket_sort


RUTA_CSV = Path("data/frecuencias_palabras.csv")
REPETICIONES = 7
EJECUCIONES_POR_MEDICION = 100


def cargar_frecuencias():
    """Carga las frecuencias numéricas del CSV."""

    with open(RUTA_CSV, "r", encoding="utf-8", newline="") as archivo:
        lector = csv.DictReader(archivo)
        return [int(fila["frecuencia"]) for fila in lector]


def medir_tiempo(algoritmo, datos):
    """Calcula la mediana del tiempo por ejecución en milisegundos."""

    # Ejecución inicial para preparar el algoritmo.
    algoritmo(datos)

    mediciones = []

    for _ in range(REPETICIONES):
        inicio = time.perf_counter()

        for _ in range(EJECUCIONES_POR_MEDICION):
            algoritmo(datos)

        fin = time.perf_counter()

        tiempo_por_ejecucion = (
            (fin - inicio) * 1000 / EJECUCIONES_POR_MEDICION
        )

        mediciones.append(tiempo_por_ejecucion)

    return median(mediciones)


def main():
    frecuencias = cargar_frecuencias()

    algoritmos = {
        "Counting Sort": counting_sort,
        "Radix Sort": radix_sort,
        "Bucket Sort": bucket_sort,
    }

    resultados = {}

    print("========== COMPARACIÓN DE ALGORITMOS ==========")
    print(f"Frecuencias procesadas: {len(frecuencias)}")
    print(f"Repeticiones por algoritmo: {REPETICIONES}")
    print(f"Ejecuciones por medición: {EJECUCIONES_POR_MEDICION}\n")

    for nombre, algoritmo in algoritmos.items():
        ordenados = algoritmo(frecuencias)

        correcto = (
            len(ordenados) == len(frecuencias)
            and all(
                ordenados[i] <= ordenados[i + 1]
                for i in range(len(ordenados) - 1)
            )
        )

        resultados[nombre] = ordenados
        tiempo = medir_tiempo(algoritmo, frecuencias)

        print(nombre)
        print(f"  Ordenamiento correcto: {correcto}")
        print(f"  Mediana por ejecución: {tiempo:.6f} ms\n")

    # Comprobamos que los tres algoritmos producen el mismo resultado.
    todos_iguales = (
        resultados["Counting Sort"] == resultados["Radix Sort"]
        == resultados["Bucket Sort"]
    )

    print(f"Los tres resultados coinciden: {todos_iguales}")


if __name__ == "__main__":
    main()
