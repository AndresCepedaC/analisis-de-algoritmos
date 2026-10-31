# Modelos preentrenados para similitud

## Selección

Los 20 abstracts están en inglés. Para que los dos métodos con embeddings sean
comparables y reproducibles, se seleccionaron modelos estáticos preentrenados
en inglés, de fuentes con licencia publicada:

| Método | Modelo | Tamaño publicado | Vocabulario y dimensión | Licencia publicada |
| --- | --- | ---: | --- | --- |
| GloVe | `glove-wiki-gigaword-50` | 69 182 535 bytes | 400 000 términos, 50 dimensiones; Wikipedia 2014 y Gigaword 5 | PDDL |
| FastText | `fasttext-wiki-news-subwords-300` | 1 005 007 116 bytes | Cerca de 1 millón de términos, 300 dimensiones; Wikipedia 2017, UMBC webbase y noticias | CC BY-SA 3.0 |

Los archivos locales se descargaron el 31 de octubre de 2026 y sus MD5 se
verificaron contra el catálogo: GloVe `c289bc5d7f2f02c6dc9f2f9b67641813`;
FastText `de2bb3a20c46ce65c9c131e1ad9a77af`.

Las fichas, fuentes y licencias se consultan en el catálogo de
[Gensim-data](https://github.com/RaRe-Technologies/gensim-data/blob/master/list.json).
Los nombres de modelo se conservan para que el informe final pueda identificar
exactamente los archivos usados.

## Archivos locales

Descargar los dos archivos de vectores en formato de texto comprimido y
guardarlos, sin descomprimir, con estos nombres:

- `data/models/glove-wiki-gigaword-50.gz`
- `data/models/fasttext-wiki-news-subwords-300.gz`

Descargas directas: [GloVe](https://github.com/RaRe-Technologies/gensim-data/releases/download/glove-wiki-gigaword-50/glove-wiki-gigaword-50.gz) y [FastText](https://github.com/RaRe-Technologies/gensim-data/releases/download/fasttext-wiki-news-subwords-300/fasttext-wiki-news-subwords-300.gz).

El programa lee `.gz` directamente. Para ahorrar memoria, procesa el archivo y
solo conserva los términos que aparecen en alguno de los 20 abstracts. El
directorio `data/models/` está excluido de Git, así que los archivos grandes no
se incorporan al repositorio.

## Alcance de cada representación

GloVe construye embeddings a partir de estadísticas globales de coocurrencia
([paper](https://nlp.stanford.edu/pubs/glove.pdf)). FastText aprende vectores a
partir de palabras y subpalabras ([vectores preentrenados](https://fasttext.cc/docs/en/english-vectors.html)). El archivo `.vec`
precomputado contiene los vectores de su vocabulario, pero no las tablas de
subpalabras del archivo binario nativo; por eso, en esta implementación, las
palabras fuera de vocabulario se omiten también para FastText. La documentación
oficial de fastText distingue los vectores `.vec` del modelo binario que permite
obtener vectores para palabras fuera del vocabulario.

Para cada abstract, el programa promedia los vectores disponibles y calcula el
coseno entre los promedios. El coseno se implementa localmente; el lector de
vectores solo proporciona las representaciones numéricas. Si un abstract no
contiene palabras presentes en el modelo, el resultado de esa medida se muestra
como no disponible.

## Reproducibilidad y comparación

En el documento final se registrarán nombre, fuente, licencia, dimensión y
fecha de descarga. También se debe reportar cuántas palabras fueron cubiertas
por cada vocabulario, ya que ese porcentaje puede explicar parte de las
diferencias entre GloVe y FastText. Las similitudes de embeddings pueden ser
negativas y no están en la misma escala que Jaccard, Dice o Levenshtein
normalizado.
