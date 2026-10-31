"""Ejecuta y mide las tres búsquedas en cada abstract original."""

from statistics import median
from time import perf_counter

from src.searching.algorithms import (
    buscar_boyer_moore,
    buscar_kmp,
    buscar_rabin_karp,
    preparar_boyer_moore,
    preparar_kmp,
    preparar_rabin_karp,
)


def comparar_patron(articulos, patron, repeticiones=7):
    """Compara métodos y usa la mediana de varias mediciones de tiempo."""
    if not patron:
        raise ValueError("El patrón de búsqueda no puede estar vacío.")
    if repeticiones < 1:
        raise ValueError("El número de repeticiones debe ser al menos 1.")

    definiciones = (
        ("KMP", preparar_kmp, buscar_kmp),
        ("Boyer-Moore", preparar_boyer_moore, buscar_boyer_moore),
        ("Rabin-Karp", preparar_rabin_karp, buscar_rabin_karp),
    )
    resultados = {}
    for nombre, preparar, buscar in definiciones:
        ocurrencias = {}
        comparaciones = 0
        colisiones = 0
        tiempos_preparacion = []
        tiempos_busqueda = []
        for _ in range(repeticiones):
            inicio_preparacion = perf_counter()
            estructura = preparar(patron)
            tiempos_preparacion.append((perf_counter() - inicio_preparacion) * 1000)

            ocurrencias_iteracion = {}
            comparaciones_iteracion = 0
            colisiones_iteracion = 0
            inicio_busqueda = perf_counter()
            for identificador in sorted(articulos):
                texto = articulos[identificador]["abstract"]
                resultado = buscar(texto, patron, estructura)
                ocurrencias_iteracion[identificador] = resultado.posiciones
                comparaciones_iteracion += resultado.comparaciones
                colisiones_iteracion += resultado.colisiones
            tiempos_busqueda.append((perf_counter() - inicio_busqueda) * 1000)
            ocurrencias = ocurrencias_iteracion
            comparaciones = comparaciones_iteracion
            colisiones = colisiones_iteracion

        resultados[nombre] = {
            "ocurrencias": ocurrencias,
            "comparaciones": comparaciones,
            "colisiones": colisiones,
            "tiempo_preparacion_ms": median(tiempos_preparacion),
            "tiempo_busqueda_ms": median(tiempos_busqueda),
            "repeticiones": repeticiones,
        }
    return resultados
