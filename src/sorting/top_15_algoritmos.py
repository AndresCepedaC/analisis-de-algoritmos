
"""
Obtiene las 15 palabras más frecuentes usando
los resultados de Counting Sort, Radix Sort y Bucket Sort.
"""

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.sorting.counting_sort import counting_sort
from src.sorting.radix_sort import radix_sort
from src.sorting.bucket_sort import bucket_sort


RUTA_ENTRADA = Path("data/frecuencias_palabras.csv")
RUTA_SALIDA = Path("data/top_15_algoritmos.csv")


def cargar_datos():
    """Lee las palabras y sus frecuencias desde el CSV."""

    palabras = []
    frecuencias = []

    with open(RUTA_ENTRADA, "r", encoding="utf-8", newline="") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            palabras.append(fila["palabra"])
            frecuencias.append(int(fila["frecuencia"]))

    return palabras, frecuencias


def obtener_top_15(palabras, frecuencias, ordenadas):
    """Recupera las palabras asociadas a las frecuencias mayores."""

    palabras_por_frecuencia = {}

    for palabra, frecuencia in zip(palabras, frecuencias):
        if frecuencia not in palabras_por_frecuencia:
            palabras_por_frecuencia[frecuencia] = []

        palabras_por_frecuencia[frecuencia].append(palabra)

    top_15 = []
    frecuencias_visitadas = set()

    # Recorremos las frecuencias de mayor a menor.
    for frecuencia in reversed(ordenadas):
        if frecuencia in frecuencias_visitadas:
            continue

        frecuencias_visitadas.add(frecuencia)

        for palabra in palabras_por_frecuencia[frecuencia]:
            top_15.append((palabra, frecuencia))

            if len(top_15) == 15:
                return top_15

    return top_15


def main():
    palabras, frecuencias = cargar_datos()

    algoritmos = {
        "Counting Sort": counting_sort,
        "Radix Sort": radix_sort,
        "Bucket Sort": bucket_sort,
    }

    resultados = {}

    for nombre, algoritmo in algoritmos.items():
        ordenadas = algoritmo(frecuencias)
        resultados[nombre] = obtener_top_15(
            palabras, frecuencias, ordenadas
        )

    # Comprobamos que los tres resultados sean iguales.
    coinciden = (
        resultados["Counting Sort"]
        == resultados["Radix Sort"]
        == resultados["Bucket Sort"]
    )

    print("========== TOP 15 POR ALGORITMO ==========")

    for nombre, top_15 in resultados.items():
        print(f"\n{nombre}")
        print(f"{'Posición':<10}{'Palabra':<20}{'Frecuencia':>12}")

        for posicion, (palabra, frecuencia) in enumerate(top_15, start=1):
            print(f"{posicion:<10}{palabra:<20}{frecuencia:>12}")

    print(f"\nLos tres resultados coinciden: {coinciden}")

    # Guardamos los resultados para el informe.
    RUTA_SALIDA.parent.mkdir(parents=True, exist_ok=True)

    with open(RUTA_SALIDA, "w", encoding="utf-8", newline="") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["algoritmo", "posicion", "palabra", "frecuencia"])

        for nombre, top_15 in resultados.items():
            for posicion, (palabra, frecuencia) in enumerate(top_15, start=1):
                escritor.writerow([nombre, posicion, palabra, frecuencia])

    print(f"Resultados guardados en: {RUTA_SALIDA}")


if __name__ == "__main__":
    main()
