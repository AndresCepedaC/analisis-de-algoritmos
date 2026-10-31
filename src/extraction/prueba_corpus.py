"""
Programa de diagnóstico para comprobar la extracción de abstracts
en todos los artículos PDF del corpus.
"""

from pathlib import Path

from pdf_reader import extraer_texto_pdf, extraer_abstract


# Carpeta que contiene los artículos científicos.
CARPETA_ARTICULOS = Path("data/articulos")


def probar_corpus():
    """Prueba la extracción de texto y abstracts de todos los PDF."""

    # Obtenemos los archivos PDF de la carpeta.
    archivos_pdf = sorted(CARPETA_ARTICULOS.glob("*.pdf"))

    if not archivos_pdf:
        print("No se encontraron archivos PDF.")
        return

    exitosos = 0
    fallidos = 0

    print(f"PDF encontrados: {len(archivos_pdf)}\n")

    # Procesamos cada archivo individualmente.
    for archivo in archivos_pdf:
        try:
            texto = extraer_texto_pdf(str(archivo))
            abstract = extraer_abstract(texto)

            if abstract:
                exitosos += 1 
                estado = "ABSTRACT encontrado"
                caracteres = len(abstract)
            else:
                fallidos += 1
                estado = "No se pudo identificar el ABSTRACT"
                caracteres = 0

            print(f"Archivo: {archivo.name}")
            print(f"Estado: {estado}")

            if abstract is None:
                print("REVISAR ESTE ARCHIVO:", archivo.name)
                
            print(f"Caracteres del abstract: {caracteres}")
            print("-" * 60)

        except Exception as error:
            fallidos += 1

            print(f"Archivo: {archivo.name}")
            print(f"Error al procesar el PDF: {error}")
            print("-" * 60)

    # Mostramos el resumen de las pruebas.
    print("\n========== RESUMEN ==========")
    print(f"Total de PDF: {len(archivos_pdf)}")
    print(f"Abstracts encontrados: {exitosos}")
    print(f"Fallos: {fallidos}")


if __name__ == "__main__":
    probar_corpus()