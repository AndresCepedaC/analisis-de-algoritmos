"""Implementaciones explícitas de cuatro medidas clásicas de similitud."""

from collections import Counter
from math import log, sqrt


def similitud_levenshtein(texto_a, texto_b):
    """Similitud normalizada por distancia de edición a nivel de carácter."""
    if texto_a == texto_b:
        return 1.0
    longitud_maxima = max(len(texto_a), len(texto_b))
    if longitud_maxima == 0:
        return 1.0

    # Una fila basta para conservar el espacio O(min(n, m)) en vez de la matriz.
    if len(texto_a) < len(texto_b):
        texto_a, texto_b = texto_b, texto_a

    fila_anterior = list(range(len(texto_b) + 1))
    for indice_a, caracter_a in enumerate(texto_a, start=1):
        fila_actual = [indice_a]
        for indice_b, caracter_b in enumerate(texto_b, start=1):
            costo = 0 if caracter_a == caracter_b else 1
            fila_actual.append(
                min(
                    fila_anterior[indice_b] + 1,
                    fila_actual[indice_b - 1] + 1,
                    fila_anterior[indice_b - 1] + costo,
                )
            )
        fila_anterior = fila_actual

    distancia = fila_anterior[-1]
    return 1.0 - distancia / longitud_maxima


def construir_tfidf(documentos):
    """Calcula TF-IDF con conteo de términos e IDF suavizado.

    El IDF usa todos los documentos del corpus aunque se comparen solo algunos.
    Cada documento se representa como un diccionario término -> peso.
    """
    conteos = [Counter(documento.split()) for documento in documentos]
    documentos_por_termino = Counter()
    for cuenta in conteos:
        documentos_por_termino.update(cuenta.keys())

    total_documentos = len(conteos)
    vectores = []
    for cuenta in conteos:
        vector = {}
        for termino, frecuencia in cuenta.items():
            idf = log((total_documentos + 1) / (documentos_por_termino[termino] + 1)) + 1
            vector[termino] = frecuencia * idf
        vectores.append(vector)
    return vectores


def similitud_coseno_vectores(vector_a, vector_b):
    """Coseno entre vectores dispersos representados como diccionarios."""
    norma_a = sqrt(sum(peso * peso for peso in vector_a.values()))
    norma_b = sqrt(sum(peso * peso for peso in vector_b.values()))
    if norma_a == 0 or norma_b == 0:
        return 0.0

    producto = sum(
        peso * vector_b.get(termino, 0.0)
        for termino, peso in vector_a.items()
    )
    return producto / (norma_a * norma_b)


def similitud_jaccard(texto_a, texto_b):
    """Jaccard entre conjuntos de términos normalizados."""
    terminos_a = set(texto_a.split())
    terminos_b = set(texto_b.split())
    union = terminos_a | terminos_b
    if not union:
        return 1.0
    return len(terminos_a & terminos_b) / len(union)


def similitud_dice(texto_a, texto_b):
    """Coeficiente Dice entre conjuntos de términos normalizados."""
    terminos_a = set(texto_a.split())
    terminos_b = set(texto_b.split())
    total = len(terminos_a) + len(terminos_b)
    if total == 0:
        return 1.0
    return 2 * len(terminos_a & terminos_b) / total


def comparar_clasicos(texto_a, texto_b, vector_tfidf_a, vector_tfidf_b):
    """Devuelve los cuatro resultados clásicos para un par de abstracts."""
    return {
        "Levenshtein normalizado": similitud_levenshtein(texto_a, texto_b),
        "Coseno TF-IDF": similitud_coseno_vectores(
            vector_tfidf_a, vector_tfidf_b
        ),
        "Jaccard": similitud_jaccard(texto_a, texto_b),
        "Dice": similitud_dice(texto_a, texto_b),
    }
