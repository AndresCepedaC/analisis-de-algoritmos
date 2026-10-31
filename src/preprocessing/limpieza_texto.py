
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

    # 1. Eliminamos el guion opcional que algunos PDF insertan dentro
    # de las palabras (por ejemplo, "educa\xadción").
    texto = texto.replace("\u00ad", "")

    # 2. Unimos palabras partidas por un salto de línea.
    # Ejemplo: "educa-\nción" -> "educación".
    texto = re.sub(r"(?<=\w)-\s*\n\s*(?=\w)", "", texto)

    # 3. Normalizamos los caracteres Unicode.
    texto = unicodedata.normalize("NFKD", texto)

    # 4. Eliminamos las tildes y marcas diacríticas.
    texto = "".join(
        caracter
        for caracter in texto
        if not unicodedata.combining(caracter)
    )

    # 5. Convertimos todo a minúsculas.
    texto = texto.lower()

    # 6. Reemplazamos la puntuación por espacios.
    texto = re.sub(r"[^\w\s]", " ", texto)

    # 7. Reducimos espacios repetidos.
    texto = re.sub(r"\s+", " ", texto).strip()

    return texto
