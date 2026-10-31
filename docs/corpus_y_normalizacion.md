# Corpus y normalización

## Fuente y organización

El corpus contiene los 20 artículos PDF de `data/articulos`. El comando
`python -m src.extraction.construir_corpus` genera `data/corpus_articulos.csv`
con una fila por artículo: identificador, nombre del PDF, título, autores,
abstract original y abstract normalizado.

Los títulos y autores se cotejaron con la portada de los PDF. No se dependió
exclusivamente de los metadatos internos, porque en varios documentos estos
omiten coautores y en el artículo 13 el título interno corresponde al nombre
del archivo de producción editorial.

## Normalización aplicada

La función `normalizar_texto` aplica las mismas reglas a todos los abstracts:

1. Elimina el guion opcional Unicode insertado dentro de palabras.
2. Une palabras cortadas con guion al final de línea.
3. Descompone caracteres Unicode y elimina marcas diacríticas.
4. Convierte el texto a minúsculas.
5. Sustituye puntuación por espacios y reduce espacios repetidos.

No elimina palabras vacías ni aplica stemming o lematización. Esto conserva el
vocabulario de origen y deja esas transformaciones como decisiones separadas
para cada algoritmo. El abstract original también se conserva para poder hacer
búsquedas exactas sin perder mayúsculas ni puntuación.

## Alcance de la validación

La extracción encontró un abstract no vacío en los 20 PDF. El generador falla
si cambia el número esperado de documentos, falta un identificador/metadato o
algún abstract no se extrae. Esta validación estructural no sustituye una
revisión editorial palabra por palabra de cada abstract.
