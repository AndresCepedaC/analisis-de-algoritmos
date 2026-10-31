
"""
Evalúa Counting Sort con las frecuencias reales
de las palabras de los abstracts.
"""

import csv
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.sorting.counting_sort import counting_sort


RUTA_CSV = Path("data/frecuencias_palabras.csv")


def evaluar_counting_sort():
    palabras = []
    frecuencias = []

    # Leemos las palabras y sus frecuencias del CSV.
    with open(RUTA_CSV, "r", encoding="utf-8", newline="") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            palabras.append(fila["palabra"])
            frecuencias.append(int(fila["frecuencia"]))

    # Medimos únicamente el tiempo del algoritmo.
    inicio = time.perf_counter()
    resultado = counting_sort(frecuencias)
    fin = time.perf_counter()

    tiempo_ms = (fin - inicio) * 1000

    # Comprobamos que el resultado esté ordenado.
    correcto = all(
        resultado[i] <= resultado[i + 1]
        for i in range(len(resultado) - 1)
    )

    print("========== EVALUACIÓN COUNTING SORT ==========")
    print(f"Palabras procesadas: {len(palabras)}")
    print(f"Ordenamiento correcto: {correcto}")
    print(f"Tiempo de ejecución: {tiempo_ms:.6f} ms")

    # Agrupamos las palabras por frecuencia.
    palabras_por_frecuencia = {}

    for palabra, frecuencia in zip(palabras, frecuencias):
        if frecuencia not in palabras_por_frecuencia:
            palabras_por_frecuencia[frecuencia] = []

        palabras_por_frecuencia[frecuencia].append(palabra)

    # Usamos el resultado del algoritmo para mostrar
    # las frecuencias mayores y sus palabras asociadas.
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
    evaluar_counting_sort()
