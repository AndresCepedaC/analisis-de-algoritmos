
from pathlib import Path
import sys

# Agregamos la raíz del proyecto a la ruta de búsqueda.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.sorting.radix_sort import radix_sort


datos = [170, 45, 75, 90, 802, 24, 2, 66]

resultado = radix_sort(datos)

print("Datos originales:", datos)
print("Datos ordenados:", resultado)

if resultado == [2, 24, 45, 66, 75, 90, 170, 802]:
    print("Prueba superada correctamente.")
else:
    print("Error en el algoritmo.")
