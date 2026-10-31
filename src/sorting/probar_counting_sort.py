
from counting_sort import counting_sort


datos = [4, 2, 4, 1, 2, 3]

resultado = counting_sort(datos)

print("Datos originales:", datos)
print("Datos ordenados:", resultado)

if resultado == [1, 2, 2, 3, 4, 4]:
    print("Prueba superada correctamente.")
else:
    print("Error en el algoritmo.")
