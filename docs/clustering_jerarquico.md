# Requerimiento 2: agrupamiento jerárquico

## Flujo

1. Leer los 20 abstracts normalizados del catálogo.
2. Representar cada abstract con los mismos pesos TF-IDF que el Requerimiento 1.
3. Calcular la distancia coseno `d(A,B) = 1 - coseno(A,B)` para cada par.
4. Ejecutar los algoritmos aglomerativos *single*, *complete* y *average*.
5. Para cada árbol, evaluar todos los cortes `k = 2..19` con silhouette.
6. Guardar un dendrograma y escoger el `k` con mayor silhouette para cada
   criterio. En empates se elige el menor `k`.

La matriz de distancia se guarda en `output/clustering/distancias_coseno.csv`.
TF-IDF e IDF se calculan sobre los 20 abstracts completos; clustering se basa
únicamente en los abstracts.

## Implementación de los enlaces

Los algoritmos están en `src/clustering/hierarchical.py`. Empiezan con un
cluster por documento. En cada iteración seleccionan la pareja de clusters con
menor distancia, la fusionan y asignan un nuevo ID al cluster. Los IDs iniciales
son `0..19`; la fusión `i` recibe el ID `20+i`. Las reglas de actualización son:

```text
single:   d(A ∪ B, C) = min(d(A,C), d(B,C))
complete: d(A ∪ B, C) = max(d(A,C), d(B,C))
average:  d(A ∪ B, C) = (|A|d(A,C) + |B|d(B,C)) / (|A|+|B|)
```

Enlaces y silhouette están implementados con estructuras básicas de Python; no
se llama a una función de clustering de SciPy o scikit-learn. La actualización
de distancias aplica estas fórmulas directamente. Para `n` documentos, buscar
la pareja mínima en cada paso cuesta `O(n³)` tiempo total y la matriz de
distancias ocupa `O(n²)` memoria.

## Evaluación interna: silhouette

Para cada documento `i`, `a(i)` es su distancia media a los demás elementos de
su grupo. `b(i)` es la menor distancia media de `i` a cualquiera de los otros
grupos. Su silhouette es:

```text
s(i) = (b(i) - a(i)) / max(a(i), b(i))
```

El promedio sobre los 20 documentos mide separación y cohesión: valores cercanos
a 1 indican grupos separados, alrededor de 0 indican fronteras entre grupos y
valores negativos indican que algunos documentos pueden quedar más cerca de
otro grupo. Un grupo unitario recibe `s(i)=0`. `src/clustering/metrics.py`
calcula la métrica directamente sobre la matriz de distancias.

Para cada enlace se prueban los 18 valores de `k` entre 2 y 19 y se reporta el
corte con mayor silhouette. La comparación entre enlaces usa el mejor promedio
de cada árbol; la métrica respalda la comparación interna, aunque no sustituye
la interpretación temática de los abstracts.

## Resultado del corpus actual

Los tres criterios obtuvieron el mismo mejor valor: `k=2` y silhouette
`0.103132`. En esos cortes, el artículo 14 queda como grupo unitario y los otros
19 artículos forman el segundo grupo. La puntuación es baja, así que la
interpretación es que TF-IDF con distancia coseno encuentra una separación
débil en este corpus temáticamente cercano. No hay un enlace ganador único con
esta representación y esta métrica; las fusiones posteriores sí difieren entre
los tres árboles.

| Enlace | Mejor k | Mejor silhouette | Lectura |
| --- | ---: | ---: | --- |
| Single | 2 | 0.103132 | Empate; artículo 14 queda solo |
| Complete | 2 | 0.103132 | Empate; artículo 14 queda solo |
| Average | 2 | 0.103132 | Empate; artículo 14 queda solo |

Este resultado se conserva sin forzar una elección: silhouette respalda un
empate y advierte que los grupos no están claramente separados bajo este
preprocesamiento.

## Dendrogramas y archivos

`src/clustering/visualization.py` dibuja los segmentos del árbol directamente a
partir del historial de fusiones; no usa un dendrograma de alto nivel. El CLI
`src/clustering/cli.py` escribe en `output/clustering/`:

- `dendrograma_single.png`, `dendrograma_complete.png` y
  `dendrograma_average.png`;
- `fusiones_<enlace>.csv`, con los nodos, alturas y tamaños de las fusiones;
- `silhouette.csv`, con la puntuación para cada enlace y cada `k`;
- `agrupaciones_mejores.csv`, con el grupo asignado a cada artículo en el mejor
  corte de cada enlace;
- `distancias_coseno.csv`, la matriz de entrada a los tres algoritmos.

Los dendrogramas muestran los IDs numéricos para mantener legibles las hojas;
`agrupaciones_mejores.csv` relaciona cada ID con su título completo.

Ejecutar `python main.py clustering` vuelve a calcular y reemplazar esos
resultados para el corpus actual.
