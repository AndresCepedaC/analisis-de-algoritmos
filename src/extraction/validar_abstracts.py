
"""
Muestra una muestra del inicio y final de cada abstract
para comprobar visualmente la extracción.
"""

from pathlib import Path

from pdf_reader import extraer_texto_pdf, extraer_abstract


CARPETA_ARTICULOS = Path("data/articulos")


def validar_abstracts():
    archivos_pdf = sorted(CARPETA_ARTICULOS.glob("*.pdf"))

    for numero, archivo in enumerate(archivos_pdf, start=1):
        texto = extraer_texto_pdf(str(archivo))
        abstract = extraer_abstract(texto)

        print("\n" + "=" * 70)
        print(f"ARTÍCULO {numero}: {archivo.name}")

        if abstract is None:
            print("ERROR: no se encontró el abstract.")
            continue

        print(f"Longitud: {len(abstract)} caracteres")
        print("\nInicio del abstract:")
        print(abstract[:250])

        print("\nFinal del abstract:")
        print(abstract[-200:])


if __name__ == "__main__":
    validar_abstracts()
