
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.sorting.bucket_sort import bucket_sort


datos = [29, 3, 15, 8, 3, 42, 17, 1]

resultado = bucket_sort(datos)

print("Datos originales:", datos)
print("Datos ordenados:", resultado)

if resultado == [1, 3, 3, 8, 15, 17, 29, 42]:
    print("Prueba superada correctamente.")
else:
    print("Error en el algoritmo.")
