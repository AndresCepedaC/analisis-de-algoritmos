
"""
Funciones para normalizar el texto de los abstracts.
"""

import re
import unicodedata


def normalizar_texto(texto):
    """
    Convierte el texto a minúsculas, elimina tildes,
    une palabras partidas por saltos de línea
    y normaliza los espacios y signos de puntuación.
    """

    # 1. Unimos palabras partidas por un salto de línea.
    # Ejemplo: "educa-\nción" -> "educación".
    texto = re.sub(r"(?<=\w)-\s*\n\s*(?=\w)", "", texto)

    # 2. Normalizamos los caracteres Unicode.
    texto = unicodedata.normalize("NFKD", texto)

    # 3. Eliminamos las tildes y marcas diacríticas.s
    texto = "".join(
        caracter
        for caracter in texto
        if not unicodedata.combining(caracter)
    )

    # 4. Convertimos todo a minúsculas.
    texto = texto.lower()

    # 5. Reemplazamos la puntuación por espacios.
    texto = re.sub(r"[^\w\s]", " ", texto)

    # 6. Reducimos espacios repetidos.
    texto = re.sub(r"\s+", " ", texto).strip()

    return texto
