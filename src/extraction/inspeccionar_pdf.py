"""
Inspecciona los encabezados de los artículos cuyo abstract
no pudo extraerse con las reglas actuales.
"""

from pathlib import Path

from pdf_reader import extraer_texto_pdf


CARPETA_ARTICULOS = Path("data/articulos")

# Nombres de archivos que fallaron en la primera prueba.
ARCHIVOS_FALLIDOS = [
    "11. A scoping review on how generative artificial intelligence transforms assessment in higher education.pdf",
    "12. A meta systematic review of artificial intelligence in higher education a call for increased ethics, collaboration, and rigour.pdf",
    "13. Artificial intelligence for education and its emphasis on assessment and adversity quotient a review.pdf",
    "14. A comprehensive exploration of artificial intelligence competence frameworks for.pdf",
    "15. A Systematic Review of Generative AI for Teaching and Learning Practice.pdf",
    "16. Generative Artificial Intelligence in Tertiary Education Assessment Redesign Principles and Considerations.pdf",
    "17. A Systematic Review of AI-Driven Educational Assessment in STEM Education.pdf",
    "18. Transforming Education A Comprehensive Review of Generative Artificial Intelligence in Educational Settings through Bibliometric and Content Analysis.pdf",
    "19. What Is the Impact of ChatGPT on Education A Rapid Review of the  Literature.pdf",
    "20. Systematic review of research on artificial intelligence applications in higher education where are the educators.pdf",
    "9. AI technologies for education Recent research  future directions.pdf",
    "7. Human-centred learning analytics and AI in education  A systematic review.pdf",
]


def inspeccionar_archivo(nombre_archivo):
    """Muestra posibles encabezados del abstract y de la introducción."""

    ruta_pdf = CARPETA_ARTICULOS / nombre_archivo

    print("\n" + "=" * 80)
    print(f"ARCHIVO: {nombre_archivo}")

    try:
        texto = extraer_texto_pdf(str(ruta_pdf))
        # Mostrar una parte más amplia del artículo 17 para localizar
        # dónde termina su abstract.
        if nombre_archivo.startswith("17."):
            print("\n========== TEXTO DEL ARTÍCULO 17 ==========\n")
            print(texto[1000:4500])
    except Exception as error:
        print(f"No se pudo leer el PDF: {error}")
        return

    # Mostrar las variantes del encabezado ABSTRACT que aparecen.
    encabezados_abstract = [
        "ABSTRACT",
        "Abstract",
        "A B S T R A C T",
        "SUMMARY",
        "Summary",
    ]

    print("\nPosibles encabezados del resumen:")

    encontrados = False

    for encabezado in encabezados_abstract:
        posicion = texto.find(encabezado)

        if posicion != -1:
            encontrados = True
            fragmento = texto[posicion:posicion + 250]

            print(f"\nCoincidencia: {encabezado!r}")
            print(fragmento.replace("\n", " "))

    if not encontrados:
        print("No se encontraron los encabezados habituales.")

    # Mostrar las posibles formas del encabezado de introducción.
    encabezados_introduccion = [
        "1. Introduction",
        "1 Introduction",
        "Introduction",
        "INTRODUCTION",
        "1. INTRODUCTION",
    ]

    print("\nPosibles encabezados de introducción:")

    encontrados = False

    for encabezado in encabezados_introduccion:
        posicion = texto.find(encabezado)

        if posicion != -1:
            encontrados = True

            print(
                f"{encabezado!r}: "
                f"posición {posicion}"
            )

    if not encontrados:
        print("No se encontraron los encabezados habituales.")


def main():
    """Inspecciona todos los archivos que fallaron."""

    for nombre_archivo in ARCHIVOS_FALLIDOS:
        inspeccionar_archivo(nombre_archivo)


if __name__ == "__main__":
    main()