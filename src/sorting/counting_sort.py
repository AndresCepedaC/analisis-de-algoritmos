
"""
Implementación de Counting Sort.

Ordena una lista de enteros no negativos
sin realizar comparaciones entre elementos.
"""


def counting_sort(datos):
    """Devuelve una nueva lista ordenada con Counting Sort."""

    if not datos:
        return []

    if any(numero < 0 for numero in datos):
        raise ValueError(
            "Counting Sort requiere enteros no negativos."
        )

    maximo = max(datos)

    # Contamos cuántas veces aparece cada valor.
    conteo = [0] * (maximo + 1)

    for numero in datos:
        conteo[numero] += 1

    # Reconstruimos la lista ordenada.
    resultado = []

    for numero, cantidad in enumerate(conteo):
        for _ in range(cantidad):
            resultado.append(numero)

    return resultado
