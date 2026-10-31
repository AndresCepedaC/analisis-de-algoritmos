
"""
Implementación de Radix Sort para enteros no negativos.

Ordena los números por sus dígitos, comenzando
por las unidades, luego las decenas y así sucesivamente.
"""


def ordenar_por_digito(datos, exponente):
    """Ordena establemente según un dígito decimal."""

    cantidad = len(datos)
    resultado = [0] * cantidad
    conteo = [0] * 10

    # Contamos las apariciones de cada dígito.
    for numero in datos:
        digito = (numero // exponente) % 10
        conteo[digito] += 1

    # Calculamos las posiciones acumuladas.
    for i in range(1, 10):
        conteo[i] += conteo[i - 1]

    # Colocamos los números de derecha a izquierda
    # para conservar la estabilidad del ordenamiento.
    for i in range(cantidad - 1, -1, -1):
        numero = datos[i]
        digito = (numero // exponente) % 10
        resultado[conteo[digito] - 1] = numero
        conteo[digito] -= 1

    return resultado


def radix_sort(datos):
    """Devuelve una nueva lista ordenada con Radix Sort."""

    if not datos:
        return []

    if any(numero < 0 for numero in datos):
        raise ValueError(
            "Radix Sort requiere enteros no negativos."
        )

    resultado = datos.copy()
    maximo = max(resultado)
    exponente = 1

    while maximo // exponente > 0:
        resultado = ordenar_por_digito(resultado, exponente)
        exponente *= 10

    return resultado
