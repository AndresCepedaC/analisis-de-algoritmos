# Análisis de Algoritmos en el contexto de la Bibliometría

Proyecto final de la asignatura Análisis de Algoritmos.

## Descripción

Aplicación para el análisis computacional de abstracts de 20 artículos científicos relacionados con Inteligencia Artificial Generativa.

## Estado del proyecto

En desarrollo.

## Requerimiento 1: similitud textual

La comparación está organizada en `src/similarity`: carga del corpus, medidas
clásicas, adaptadores de embeddings, servicio de comparación e interfaz CLI.
Los algoritmos clásicos están implementados en el proyecto. Los modelos
preentrenados no se incluyen en el repositorio.

Para comparar los abstracts de los artículos 1 y 2 con las cuatro medidas
clásicas:

```powershell
python main.py --ids 1 2
```

Para comparar con todos los métodos, se requieren además archivos locales de
GloVe y FastText en formato de vectores de texto:

```powershell
python main.py --ids 1 2 --glove data/models/glove-wiki-gigaword-50.gz --fasttext data/models/fasttext-wiki-news-subwords-300.gz
```

`--salida ruta.csv` exporta los resultados. La documentación del módulo está
en `docs/similitud_textual.md`; las fuentes y condiciones de los modelos están
en `docs/modelos_embeddings.md`. El cálculo detallado para los artículos 1 y 10
está en `docs/caso_estudio_similitud.md`.

## Requerimiento 2: clustering jerárquico

El clustering usa distancia coseno sobre TF-IDF y construye desde cero los
árboles *single*, *complete* y *average linkage*. Ejecuta:

```powershell
python main.py clustering
```

El comando guarda los tres dendrogramas, las fusiones, la matriz de distancias,
las puntuaciones silhouette y las asignaciones del mejor corte en
`output/clustering/`. La metodología está en `docs/clustering_jerarquico.md`.

## Requerimiento 3: búsqueda de cadenas

La búsqueda exacta se ejecuta sobre los abstracts originales, distingue
mayúsculas y conserva puntuación y saltos de línea. Para buscar `AI`:

```powershell
python main.py busqueda --patron "AI" --repeticiones 7
```

Las posiciones y las medianas de siete mediciones separadas de
preprocesamiento/búsqueda se guardan en `output/searching/`. La implementación y el caso de estudio están
documentados en `docs/busqueda_cadenas.md`.
