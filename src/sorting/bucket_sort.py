
"""
Implementación de Bucket Sort para enteros no negativos.
"""


def bucket_sort(datos):
    """Devuelve una nueva lista ordenada con Bucket Sort."""

    if not datos:
        return []

    if any(numero < 0 for numero in datos):
        raise ValueError(
            "Bucket Sort requiere enteros no negativos."
        )

    minimo = min(datos)
    maximo = max(datos)

    cantidad_buckets = len(datos)
    buckets = [[] for _ in range(cantidad_buckets)]

    # Distribuimos los números en los buckets.
    rango = maximo - minimo + 1

    for numero in datos:
        indice = (numero - minimo) * cantidad_buckets // rango
        indice = min(indice, cantidad_buckets - 1)
        buckets[indice].append(numero)

    # Ordenamos cada bucket mediante inserción.
    resultado = []

    for bucket in buckets:
        for i in range(1, len(bucket)):
            actual = bucket[i]
            j = i - 1

            while j >= 0 and bucket[j] > actual:
                bucket[j + 1] = bucket[j]
                j -= 1

            bucket[j + 1] = actual

        resultado.extend(bucket)

    return resultado
