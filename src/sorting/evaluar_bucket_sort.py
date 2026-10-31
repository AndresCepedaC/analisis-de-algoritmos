
"""
Evalúa Bucket Sort con las frecuencias reales
de las palabras de los abstracts.
"""

import csv
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.sorting.bucket_sort import bucket_sort


RUTA_CSV = Path("data/frecuencias_palabras.csv")


def evaluar_bucket_sort():
    palabras = []
    frecuencias = []

    # Leemos las palabras y sus frecuencias.
    with open(RUTA_CSV, "r", encoding="utf-8", newline="") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            palabras.append(fila["palabra"])
            frecuencias.append(int(fila["frecuencia"]))

    # Medimos solamente el tiempo de ordenamiento.
    inicio = time.perf_counter()
    resultado = bucket_sort(frecuencias)
    fin = time.perf_counter()

    tiempo_ms = (fin - inicio) * 1000

    correcto = all(
        resultado[i] <= resultado[i + 1]
        for i in range(len(resultado) - 1)
    )

    print("========== EVALUACIÓN BUCKET SORT ==========")
    print(f"Palabras procesadas: {len(frecuencias)}")
    print(f"Ordenamiento correcto: {correcto}")
    print(f"Tiempo de ejecución: {tiempo_ms:.6f} ms")

    # Asociamos cada frecuencia con sus palabras.
    palabras_por_frecuencia = {}

    for palabra, frecuencia in zip(palabras, frecuencias):
        if frecuencia not in palabras_por_frecuencia:
            palabras_por_frecuencia[frecuencia] = []

        palabras_por_frecuencia[frecuencia].append(palabra)

    # Mostramos las palabras con las frecuencias más altas.
    print("\n15 palabras más frecuentes:")
    mostradas = 0
    frecuencias_visitadas = set()

    for frecuencia in reversed(resultado):
        if frecuencia in frecuencias_visitadas:
            continue

        frecuencias_visitadas.add(frecuencia)

        for palabra in palabras_por_frecuencia[frecuencia]:
            print(f"{palabra}: {frecuencia}")
            mostradas += 1

            if mostradas == 15:
                break

        if mostradas == 15:
            break


if __name__ == "__main__":
    evaluar_bucket_sort()
