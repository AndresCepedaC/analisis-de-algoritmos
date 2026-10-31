
"""
Calcula la frecuencia de las palabras de los abstracts
de los artículos científicos del corpus.
"""
from collections import Counter
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.preprocessing.limpieza_texto import normalizar_texto
from src.extraction.pdf_reader import extraer_texto_pdf, extraer_abstract

CARPETA_ARTICULOS = Path("data/articulos")


def calcular_frecuencias():
    """Extrae los abstracts y cuenta las palabras."""

    frecuencias = Counter()
    articulos_procesados = 0

    archivos_pdf = sorted(CARPETA_ARTICULOS.glob("*.pdf"))

    for archivo in archivos_pdf:
        texto_pdf = extraer_texto_pdf(str(archivo))
        abstract = extraer_abstract(texto_pdf)

        if abstract is None:
            print(f"No se pudo extraer el abstract: {archivo.name}")
            continue

        texto_limpio = normalizar_texto(abstract)
        palabras = texto_limpio.split()

        frecuencias.update(palabras)
        articulos_procesados += 1

    return frecuencias, articulos_procesados, len(archivos_pdf)


if __name__ == "__main__":
    frecuencias, procesados, total = calcular_frecuencias()

    print(f"PDF encontrados: {total}")
    print(f"Artículos procesados: {procesados}")
    print(f"Palabras diferentes: {len(frecuencias)}")

    print("\n15 palabras más frecuentes:")

    for palabra, cantidad in frecuencias.most_common(15):
        print(f"{palabra}: {cantidad}")
