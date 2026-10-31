
"""
Evalúa Radix Sort con las frecuencias reales
de las palabras de los abstracts.
"""

import csv
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.sorting.radix_sort import radix_sort

RUTA_CSV = Path("data/frecuencias_palabras.csv")

def evaluar_radix_sort():
    frecuencias = []

    # Leemos las frecuencias del archivo CSV.
    with open(RUTA_CSV, "r", encoding="utf-8", newline="") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            frecuencias.append(int(fila["frecuencia"]))

    # Medimos únicamente el tiempo de ordenamiento.
    inicio = time.perf_counter()
    resultado = radix_sort(frecuencias)
    fin = time.perf_counter()

    tiempo_ms = (fin - inicio) * 1000

    correcto = all(
        resultado[i] <= resultado[i + 1]
        for i in range(len(resultado) - 1)
    )

    print("========== EVALUACIÓN RADIX SORT ==========")
    print(f"Palabras procesadas: {len(frecuencias)}")
    print(f"Ordenamiento correcto: {correcto}")
    print(f"Tiempo de ejecución: {tiempo_ms:.6f} ms")


if __name__ == "__main__":
    evaluar_radix_sort()
