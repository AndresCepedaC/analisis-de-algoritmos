
"""
Guarda las frecuencias de las palabras en un archivo CSV.
"""

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.preprocessing.frecuencia_palabras import calcular_frecuencias


def guardar_frecuencias():
    frecuencias, procesados, total = calcular_frecuencias()

    carpeta_salida = Path("data")
    carpeta_salida.mkdir(exist_ok=True)

    ruta_salida = carpeta_salida / "frecuencias_palabras.csv"

    with open(ruta_salida, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["palabra", "frecuencia"])

        for palabra, cantidad in frecuencias.items():
            escritor.writerow([palabra, cantidad])

    print(f"Artículos procesados: {procesados}/{total}")
    print(f"Palabras diferentes: {len(frecuencias)}")
    print(f"Archivo guardado en: {ruta_salida}")


if __name__ == "__main__":
    guardar_frecuencias()
