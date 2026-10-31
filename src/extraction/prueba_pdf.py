"""
Programa de prueba para verificar la extracción de texto y abstract
de un artículo científico en formato PDF.

Este archivo se utiliza durante el desarrollo para comprobar que
pdf_reader.py funciona correctamente.
"""

from pdf_reader import extraer_texto_pdf, extraer_abstract


# -------------------------------------------------------------------
# CONFIGURACIÓN
# -------------------------------------------------------------------

# Ruta del artículo que utilizaremos para realizar la prueba.
ruta_pdf = (
    "data/articulos/"
    "1. Artificial intelligence literacy in higher and adult education "
    "A scoping literature review.pdf"
)

# -------------------------------------------------------------------
# EXTRACCIÓN DEL TEXTO
# -------------------------------------------------------------------

# Extraemos todo el texto contenido en el PDF.
texto = extraer_texto_pdf(ruta_pdf)

print("PDF procesado correctamente.")
print("Cantidad de caracteres del documento:", len(texto))

# -------------------------------------------------------------------
# EXTRACCIÓN DEL ABSTRACT
# -------------------------------------------------------------------

# Intentamos obtener únicamente el abstract.
abstract = extraer_abstract(texto)


# -------------------------------------------------------------------
# RESULTADOS
# -------------------------------------------------------------------

if abstract is not None:

    print("\n========== ABSTRACT EXTRAÍDO ==========\n")
    print(abstract)

    print("\n========================================")
    print("Cantidad de caracteres del abstract:", len(abstract))

else:

    print("\nNo fue posible extraer el abstract.")