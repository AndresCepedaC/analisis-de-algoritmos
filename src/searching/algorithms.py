"""Tres algoritmos explícitos de coincidencia exacta de cadenas."""

from typing import NamedTuple


class ResultadoBusqueda(NamedTuple):
    posiciones: list
    comparaciones: int
    colisiones: int


def preparar_kmp(patron):
    """Calcula la tabla LPS (prefijo propio más largo que también es sufijo)."""
    _validar_patron(patron)
    lps = [0] * len(patron)
    longitud = 0
    indice = 1
    while indice < len(patron):
        if patron[indice] == patron[longitud]:
            longitud += 1
            lps[indice] = longitud
            indice += 1
        elif longitud > 0:
            longitud = lps[longitud - 1]
        else:
            lps[indice] = 0
            indice += 1
    return lps


def buscar_kmp(texto, patron, lps):
    """Busca todas las coincidencias con Knuth-Morris-Pratt."""
    _validar_patron(patron)
    posiciones = []
    comparaciones = 0
    indice_texto = 0
    indice_patron = 0

    while indice_texto < len(texto):
        comparaciones += 1
        if texto[indice_texto] == patron[indice_patron]:
            indice_texto += 1
            indice_patron += 1
            if indice_patron == len(patron):
                posiciones.append(indice_texto - indice_patron)
                indice_patron = lps[indice_patron - 1]
        elif indice_patron > 0:
            indice_patron = lps[indice_patron - 1]
        else:
            indice_texto += 1

    return ResultadoBusqueda(posiciones, comparaciones, 0)


def preparar_boyer_moore(patron):
    """Construye la tabla de última aparición para la regla del carácter malo."""
    _validar_patron(patron)
    ultima_aparicion = {}
    for indice, caracter in enumerate(patron):
        ultima_aparicion[caracter] = indice
    return ultima_aparicion


def buscar_boyer_moore(texto, patron, ultima_aparicion):
    """Busca de derecha a izquierda y desplaza con la regla del carácter malo."""
    _validar_patron(patron)
    posiciones = []
    comparaciones = 0
    desplazamiento = 0
    longitud_patron = len(patron)

    while desplazamiento <= len(texto) - longitud_patron:
        indice_patron = longitud_patron - 1
        while indice_patron >= 0:
            comparaciones += 1
            if patron[indice_patron] != texto[desplazamiento + indice_patron]:
                break
            indice_patron -= 1

        if indice_patron < 0:
            posiciones.append(desplazamiento)
            # Un desplazamiento de 1 conserva las coincidencias que se solapan.
            desplazamiento += 1
        else:
            caracter_malo = texto[desplazamiento + indice_patron]
            ultima = ultima_aparicion.get(caracter_malo, -1)
            desplazamiento += max(1, indice_patron - ultima)

    return ResultadoBusqueda(posiciones, comparaciones, 0)


BASE_HASH = 256
MODULO_HASH = 1_000_000_007


class PreparacionRabinKarp(NamedTuple):
    hash_patron: int
    potencia_mas_alta: int


def preparar_rabin_karp(patron):
    """Calcula hash polinómico y potencia para actualizar la ventana."""
    _validar_patron(patron)
    hash_patron = 0
    for caracter in patron:
        hash_patron = (BASE_HASH * hash_patron + ord(caracter)) % MODULO_HASH
    potencia = pow(BASE_HASH, len(patron) - 1, MODULO_HASH)
    return PreparacionRabinKarp(hash_patron, potencia)


def buscar_rabin_karp(texto, patron, preparacion):
    """Busca ventanas con rolling hash y verifica cada posible coincidencia."""
    _validar_patron(patron)
    longitud_patron = len(patron)
    if longitud_patron > len(texto):
        return ResultadoBusqueda([], 0, 0)

    hash_ventana = 0
    for indice in range(longitud_patron):
        hash_ventana = (
            BASE_HASH * hash_ventana + ord(texto[indice])
        ) % MODULO_HASH

    posiciones = []
    comparaciones = 0
    colisiones = 0
    for inicio in range(len(texto) - longitud_patron + 1):
        if hash_ventana == preparacion.hash_patron:
            indice = 0
            while indice < longitud_patron:
                comparaciones += 1
                if texto[inicio + indice] != patron[indice]:
                    colisiones += 1
                    break
                indice += 1
            if indice == longitud_patron:
                posiciones.append(inicio)

        if inicio < len(texto) - longitud_patron:
            hash_ventana = (
                BASE_HASH
                * (hash_ventana - ord(texto[inicio]) * preparacion.potencia_mas_alta)
                + ord(texto[inicio + longitud_patron])
            ) % MODULO_HASH

    return ResultadoBusqueda(posiciones, comparaciones, colisiones)


def _validar_patron(patron):
    if not patron:
        raise ValueError("El patrón de búsqueda no puede estar vacío.")
