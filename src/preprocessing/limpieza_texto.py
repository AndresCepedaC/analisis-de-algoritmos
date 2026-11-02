"""Normalización de abstracts y tokenización léxica para conteos."""

from __future__ import annotations

import logging
import re
import unicodedata

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Stopwords del inglés — se obtienen de NLTK (requisito académico).
# Si NLTK no está instalado o el recurso no se ha descargado, se usa un
# conjunto de respaldo equivalente para no bloquear la ejecución.
# ---------------------------------------------------------------------------

_STOPWORDS_RESPALDO: frozenset[str] = frozenset(
    {
        "a",
        "about",
        "above",
        "after",
        "again",
        "against",
        "ain",
        "all",
        "am",
        "an",
        "and",
        "any",
        "are",
        "aren",
        "arent",
        "as",
        "at",
        "be",
        "because",
        "been",
        "before",
        "being",
        "below",
        "between",
        "both",
        "but",
        "by",
        "can",
        "couldn",
        "couldnt",
        "d",
        "did",
        "didn",
        "didnt",
        "do",
        "does",
        "doesn",
        "doesnt",
        "doing",
        "don",
        "dont",
        "down",
        "during",
        "each",
        "few",
        "for",
        "from",
        "further",
        "had",
        "hadn",
        "hadnt",
        "has",
        "hasn",
        "hasnt",
        "have",
        "haven",
        "havent",
        "having",
        "he",
        "her",
        "here",
        "hers",
        "herself",
        "him",
        "himself",
        "his",
        "how",
        "i",
        "if",
        "in",
        "into",
        "is",
        "isn",
        "isnt",
        "it",
        "its",
        "itself",
        "just",
        "ll",
        "m",
        "ma",
        "me",
        "mightn",
        "mightnt",
        "more",
        "most",
        "mustn",
        "mustnt",
        "my",
        "myself",
        "needn",
        "neednt",
        "no",
        "nor",
        "not",
        "now",
        "o",
        "of",
        "off",
        "on",
        "once",
        "only",
        "or",
        "other",
        "our",
        "ours",
        "ourselves",
        "out",
        "over",
        "own",
        "re",
        "s",
        "same",
        "shan",
        "shant",
        "she",
        "shes",
        "should",
        "shouldn",
        "shouldnt",
        "shouldve",
        "so",
        "some",
        "such",
        "t",
        "than",
        "that",
        "thatll",
        "the",
        "their",
        "theirs",
        "them",
        "themselves",
        "then",
        "there",
        "these",
        "they",
        "this",
        "those",
        "through",
        "to",
        "too",
        "under",
        "until",
        "up",
        "ve",
        "very",
        "was",
        "wasn",
        "wasnt",
        "we",
        "were",
        "weren",
        "werent",
        "what",
        "when",
        "where",
        "which",
        "while",
        "who",
        "whom",
        "why",
        "will",
        "with",
        "won",
        "wont",
        "wouldn",
        "wouldnt",
        "y",
        "you",
        "youd",
        "youll",
        "your",
        "youre",
        "yours",
        "yourself",
        "yourselves",
        "youve",
    }
)


def _cargar_stopwords() -> frozenset[str]:
    """Carga stopwords desde NLTK; usa respaldo si no está disponible."""
    try:
        from nltk.corpus import stopwords  # noqa: WPS433 — import dentro de función

        palabras = frozenset(stopwords.words("english"))
        logger.info("Stopwords cargadas desde NLTK (%d palabras).", len(palabras))
        return palabras
    except (ImportError, LookupError):
        logger.warning(
            "NLTK no disponible o recurso 'stopwords' no descargado. "
            "Se usa el conjunto de respaldo (%d palabras). "
            "Ejecuta: python -m nltk.downloader stopwords",
            len(_STOPWORDS_RESPALDO),
        )
        return _STOPWORDS_RESPALDO


STOPWORDS_INGLES: frozenset[str] = _cargar_stopwords()

# ---------------------------------------------------------------------------
# Regex: captura ÚNICAMENTE palabras alfabéticas (incluye acentos y ñ),
# excluyendo dígitos numéricos y guiones bajos.
# Se usan word boundaries (\b) para delimitar tokens completos.
# ---------------------------------------------------------------------------
_PATRON_ALFABETICO = re.compile(r"(?<![a-záéíóúñ])[a-záéíóúñ]+(?![a-záéíóúñ])")


_MARCADOR_ENIE = "\x02ENIE\x03"


def _preservar_enie(texto: str) -> str:
    """Reemplaza ñ/Ñ por un marcador ASCII antes de eliminar diacríticos.

    La ñ en Unicode se descompone como n + combining tilde (~), por lo que
    la eliminación de caracteres combinantes la destruye. Este paso la
    protege con un marcador que no contiene caracteres combinantes.
    """
    return texto.replace("ñ", _MARCADOR_ENIE).replace("Ñ", _MARCADOR_ENIE)


def _restaurar_enie(texto: str) -> str:
    """Restaura los marcadores a la letra ñ real."""
    return texto.replace(_MARCADOR_ENIE, "ñ")


def normalizar_texto(texto: str | None) -> str:
    """Convierte un abstract a minúsculas y deja solo palabras alfabéticas.

    Pasos:
        1. Une cortes de línea con guion (hyphenation).
        2. Pasa a minúsculas.
        3. Preserva la ñ antes de eliminar diacríticos.
        4. Normaliza NFKD y elimina caracteres combinantes (tildes).
        5. Restaura la ñ.
        6. Extrae tokens con ``\\b[a-záéíóúñ]+\\b`` (sin dígitos ni guiones
           bajos).

    Args:
        texto: Abstract original o cadena vacía.

    Returns:
        Texto normalizado separado por espacios. Cadena vacía si el
        argumento es nulo o no contiene letras.

    Raises:
        TypeError: Si el valor no es una cadena ni ``None``.
    """
    if texto is None:
        logger.warning("Se recibió texto nulo; se normaliza como cadena vacía.")
        return ""
    if not isinstance(texto, str):
        raise TypeError(f"El texto debe ser str o None, no {type(texto).__name__}.")

    # Eliminar soft hyphens.
    texto = texto.replace("\u00ad", "")
    # Unir palabras cortadas por guion al final de línea.
    texto = re.sub(r"(?<=\w)-\s*\n\s*(?=\w)", "", texto)
    # Minúsculas primero para simplificar el resto del pipeline.
    texto = texto.lower()
    # Proteger la ñ antes de la descomposición NFKD.
    texto = _preservar_enie(texto)
    # Descomponer y eliminar diacríticos (tildes combinantes).
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(
        caracter for caracter in texto if not unicodedata.combining(caracter)
    )
    # Restaurar la ñ protegida.
    texto = _restaurar_enie(texto)
    # Extraer únicamente tokens alfabéticos con word boundaries.
    tokens = _PATRON_ALFABETICO.findall(texto)
    return " ".join(tokens)


def eliminar_stopwords(tokens: list[str]) -> list[str]:
    """Filtra palabras vacías del inglés usando NLTK (o respaldo).

    Args:
        tokens: Palabras ya en minúsculas y solo alfabéticas.

    Returns:
        Tokens que no pertenecen a ``STOPWORDS_INGLES``.
    """
    if not tokens:
        return []
    return [token for token in tokens if token not in STOPWORDS_INGLES]


def tokenizar_para_frecuencias(texto: str | None) -> list[str]:
    """Normaliza, extrae tokens alfabéticos y quita stopwords.

    Args:
        texto: Abstract original.

    Returns:
        Lista de términos de contenido, lista para contar frecuencias.
    """
    texto_limpio = normalizar_texto(texto)
    if not texto_limpio:
        return []
    return eliminar_stopwords(texto_limpio.split())
