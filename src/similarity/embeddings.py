"""Carga selectiva de embeddings preentrenados y comparación por coseno.

Los dos modelos se leen desde archivos de texto con cabecera. Solo se guardan
en memoria los vectores de las palabras que aparecen en el corpus del proyecto.
"""

import gzip
from math import sqrt
from pathlib import Path


class VectorStore:
    """Conjunto mínimo de vectores requerido por el comparador."""

    def __init__(self, vector_size, vectors):
        self.vector_size = vector_size
        self.vectors = vectors
        self.key_to_index = {token: indice for indice, token in enumerate(vectors)}

    def __getitem__(self, token):
        return self.vectors[token]


def _cargar_vectores_texto(ruta, vocabulario):
    """Lee texto vectorial con cabecera y conserva solo el vocabulario pedido."""
    ruta = Path(ruta)
    if not ruta.is_file():
        raise FileNotFoundError(f"No se encontró el archivo de embeddings: {ruta}")

    abrir = gzip.open if ruta.suffix.lower() == ".gz" else open
    vectores = {}
    dimension = None
    with abrir(ruta, "rt", encoding="utf-8", errors="replace") as archivo:
        primera_linea = archivo.readline()
        campos = primera_linea.split()
        tiene_cabecera = (
            len(campos) == 2
            and campos[0].isdigit()
            and campos[1].isdigit()
        )
        if tiene_cabecera:
            dimension = int(campos[1])
        else:
            if len(campos) < 2:
                raise ValueError(f"No se pudo leer la dimensión de los vectores en {ruta}.")
            token = campos[0]
            valores = " ".join(campos[1:])
            dimension = len(campos) - 1
            _guardar_vector(token, valores, dimension, vocabulario, vectores, ruta, 1)

        for numero_linea, linea in enumerate(archivo, start=2):
            campos = linea.split(maxsplit=1)
            if not campos:
                continue
            if len(campos) != 2:
                raise ValueError(
                    f"Formato vectorial inválido en {ruta}, línea {numero_linea}."
                )
            _guardar_vector(
                campos[0], campos[1], dimension, vocabulario, vectores, ruta, numero_linea
            )

    if not vectores:
        raise ValueError(
            f"El modelo {ruta.name} no contiene vectores para palabras del corpus."
        )
    return VectorStore(dimension, vectores)


def _guardar_vector(token, texto_vector, dimension, vocabulario, vectores, ruta, numero_linea):
    if token not in vocabulario:
        return
    valores = texto_vector.split()
    if len(valores) != dimension:
        raise ValueError(
            f"Formato vectorial inválido en {ruta}, línea {numero_linea}: "
            f"se esperaban {dimension} valores numéricos."
        )
    try:
        vectores[token] = [float(valor) for valor in valores]
    except ValueError as error:
        raise ValueError(
            f"Vector no numérico para '{token}' en {ruta}, línea {numero_linea}."
        ) from error


def cargar_glove(ruta, vocabulario):
    """Carga vectores GloVe en formato texto, opcionalmente comprimidos en gzip."""
    return _cargar_vectores_texto(ruta, vocabulario)


def cargar_fasttext(ruta, vocabulario):
    """Carga vectores FastText precomputados desde un archivo `.vec` de texto."""
    return _cargar_vectores_texto(ruta, vocabulario)


def vector_promedio(texto, vectores):
    """Promedia los vectores de cada token; omite tokens sin representación."""
    acumulado = [0.0] * vectores.vector_size
    cantidad = 0
    for token in texto.split():
        if token not in vectores.key_to_index:
            continue
        try:
            vector = vectores[token]
        except (KeyError, ValueError):
            continue
        for indice, valor in enumerate(vector):
            acumulado[indice] += float(valor)
        cantidad += 1

    if cantidad == 0:
        return None
    return [valor / cantidad for valor in acumulado]


def cobertura_vocabulario(texto, vectores):
    """Cuenta tokens del texto que tienen vector en el modelo."""
    tokens = texto.split()
    cubiertos = sum(token in vectores.key_to_index for token in tokens)
    return cubiertos, len(tokens)


def coseno_denso(vector_a, vector_b):
    """Calcula coseno con listas de números, sin delegar la métrica."""
    if len(vector_a) != len(vector_b):
        raise ValueError("Los embeddings deben tener la misma dimensión.")
    producto = sum(a * b for a, b in zip(vector_a, vector_b))
    norma_a = sqrt(sum(valor * valor for valor in vector_a))
    norma_b = sqrt(sum(valor * valor for valor in vector_b))
    if norma_a == 0 or norma_b == 0:
        return None
    return producto / (norma_a * norma_b)


def similitud_embeddings(texto_a, texto_b, vectores):
    """Similitud coseno entre promedios de embeddings de dos abstracts."""
    vector_a = vector_promedio(texto_a, vectores)
    vector_b = vector_promedio(texto_b, vectores)
    if vector_a is None or vector_b is None:
        return None
    return coseno_denso(vector_a, vector_b)
