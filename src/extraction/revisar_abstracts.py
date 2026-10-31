
"""
Inspecciona el inicio de los cuatro PDF cuyo abstract falla.
"""

from pathlib import Path

from pdf_reader import extraer_texto_pdf


CARPETA_ARTICULOS = Path("data/articulos")

ARTICULOS_REVISAR = [
    "7. Human-centred learning analytics and AI in education  A systematic review.pdf",
    "9. AI technologies for education Recent research  future directions.pdf",
    "14. A comprehensive exploration of artificial intelligence competence frameworks for.pdf",
    "17. A Systematic Review of AI-Driven Educational Assessment in STEM Education.pdf",
]


def inspeccionar(nombre_archivo):
    ruta = CARPETA_ARTICULOS / nombre_archivo
    texto = extraer_texto_pdf(str(ruta))

    print("\n" + "=" * 80)
    print(f"ARCHIVO: {nombre_archivo}")
    print("=" * 80)

    # Mostramos el inicio del documento para observar su estructura.
    print(texto[:4500])


def main():
    for archivo in ARTICULOS_REVISAR:
        inspeccionar(archivo)


if __name__ == "__main__":
    main()
