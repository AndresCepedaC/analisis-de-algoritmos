# Caso de estudio: similitud entre dos abstracts

## Artículos seleccionados

Se comparan los abstracts de los artículos 1 y 10:

1. **Artificial intelligence literacy in higher and adult education: A scoping literature review**
2. **Educational applications of artificial intelligence in simulation-based learning: A systematic mapping review**

Los dos tratan IA en educación, pero desde focos diferentes: alfabetización en
IA y aprendizaje basado en simulación. Esto permite observar qué captan los
métodos de coincidencia de términos y qué captan los embeddings.

Los resultados completos se guardan en `data/resultados_similitud_1_10.csv`.
Los abstracts normalizados tienen 1129 y 1399 caracteres, y 189 y 210 tokens,
respectivamente.

## Resultados

| Método | Similitud |
| --- | ---: |
| Levenshtein normalizado | 0.304503 |
| Coseno TF-IDF | 0.252435 |
| Jaccard | 0.126214 |
| Dice | 0.224138 |
| GloVe (coseno) | 0.983108 |
| FastText (coseno) | 0.970645 |

Cobertura de los modelos: GloVe representa 189/189 tokens del artículo 1 y
209/210 del artículo 10; FastText representa 189/189 y 210/210. Los dos modelos
recibieron los mismos abstracts normalizados.

## Levenshtein

Para los abstracts completos, la comparación es carácter por carácter. Si sus
longitudes son `n = 1129` y `m = 1399`, la programación dinámica calcula una
distancia de edición `d = 973`. La conversión a similitud es:

```text
similitud = 1 - d / max(n, m)
          = 1 - 973 / 1399
          = 0.304503
```

La matriz completa tendría más de 1.5 millones de celdas. Para mostrar la
recurrencia en una tabla legible, se usan dos términos presentes en los
abstracts: `literacy` (artículo 1) y `learning` (artículo 10). En ambos casos,
las filas y columnas son caracteres. Se inicializa `D[i,0] = i` y `D[0,j] = j`;
cada celda se obtiene con:

```text
D[i,j] = min(
    D[i-1,j] + 1,          eliminación,
    D[i,j-1] + 1,          inserción,
    D[i-1,j-1] + costo     sustitución o coincidencia
)
costo = 0 si los caracteres son iguales; 1 en otro caso.
```

|   | ε | l | e | a | r | n | i | n | g |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| ε | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| l | 1 | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| i | 2 | 1 | 1 | 2 | 3 | 4 | 4 | 5 | 6 |
| t | 3 | 2 | 2 | 2 | 3 | 4 | 5 | 5 | 6 |
| e | 4 | 3 | 2 | 3 | 3 | 4 | 5 | 6 | 6 |
| r | 5 | 4 | 3 | 3 | 3 | 4 | 5 | 6 | 7 |
| a | 6 | 5 | 4 | 3 | 4 | 4 | 5 | 6 | 7 |
| c | 7 | 6 | 5 | 4 | 4 | 5 | 5 | 6 | 7 |
| y | 8 | 7 | 6 | 5 | 5 | 5 | 6 | 6 | 7 |

La celda final `D[8,8] = 7` indica siete operaciones para transformar el término
`literacy` en `learning`. Esta matriz pequeña ilustra la misma regla usada para
los abstracts completos; el puntaje de la tabla anterior sí se calculó sobre
los dos abstracts completos.

## TF-IDF y coseno

Para cada término `t`, se usa `TF(t,d) = frecuencia(t,d)` e
`IDF(t) = ln((N+1)/(df(t)+1)) + 1`, con `N = 20` abstracts. Por ejemplo,
`education` aparece 3 veces en el artículo 1, 2 veces en el artículo 10 y en
`df = 18` abstracts:

```text
IDF(education) = ln(21/19) + 1 = 1.100083
TF-IDF(education, artículo 1)  = 3 × 1.100083 = 3.300250
TF-IDF(education, artículo 10) = 2 × 1.100083 = 2.200167
```

En cambio, `simulation` aparece 6 veces en el artículo 10 y solo en un abstract
del corpus; por eso recibe `IDF = ln(21/2)+1 = 3.351375` y peso `20.108251` en
el artículo 10. El coseno se calcula con todos los términos y vectores dispersos:

```text
producto punto = 512.273694
norma artículo 1 = 39.999421
norma artículo 10 = 50.733901
coseno = 512.273694 / (39.999421 × 50.733901) = 0.252435
```

## Jaccard y Dice

Se convierten los abstracts normalizados en conjuntos; por tanto, las
repeticiones no incrementan el tamaño. El artículo 1 tiene 118 términos únicos,
el artículo 10 tiene 114 y comparten 26. La unión tiene 206 términos:

```text
Jaccard = |A ∩ B| / |A ∪ B| = 26 / 206 = 0.126214
Dice    = 2|A ∩ B| / (|A| + |B|) = 52 / 232 = 0.224138
```

## Embeddings y lectura crítica

Para cada modelo se promedian los vectores de todos los tokens cubiertos en
cada abstract y luego se calcula el coseno entre los dos promedios. El resultado
GloVe es `0.983108`; FastText da `0.970645`. Ambos detectan una relación
semántica fuerte, aunque los métodos léxicos producen valores mucho menores.

El detalle numérico reproducible para los promedios es:

| Modelo | Dimensiones | Tokens cubiertos (art. 1 / 10) | Producto punto | Norma art. 1 | Norma art. 10 | Coseno |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| GloVe | 50 | 189/189, 209/210 | 12.050689 | 3.655881 | 3.352884 | 0.983108 |
| FastText | 300 | 189/189, 210/210 | 0.364500 | 0.653788 | 0.574381 | 0.970645 |

Los promedios son vectores `v̄ = (1/r) Σ v(w)` sobre los `r` tokens cubiertos.
Para ilustrar su construcción, las primeras cinco coordenadas de GloVe son
`v̄₁ = (0.297351, 0.153013, -0.083919, -0.105727, 0.244577, …)` y
`v̄₁₀ = (0.257146, 0.177087, -0.126414, 0.063347, 0.098717, …)`. Para
FastText, las primeras cinco son `v̄₁ = (0.001246, -0.015115, 0.018668,
0.006588, -0.010064, …)` y `v̄₁₀ = (0.006663, -0.015334, 0.011097,
0.008928, -0.023486, …)`. Los puntos suspensivos representan las coordenadas
restantes, incluidas en las normas y productos punto de la tabla.

En ambos casos se aplica `cos(v̄₁,v̄₁₀) = (v̄₁ · v̄₁₀) / (||v̄₁|| ||v̄₁₀||)`.
Para GloVe, `12.050689 / (3.655881 × 3.352884) = 0.983108`; para FastText,
`0.364500 / (0.653788 × 0.574381) = 0.970645` (las diferencias en el último
decimal dependen del redondeo mostrado). El cálculo se realizó sobre todos los
50 o 300 componentes, respectivamente, no solo los cinco que se imprimen como
ilustración.

La diferencia no significa que una escala sea universalmente mejor. Jaccard,
Dice, TF-IDF y Levenshtein dependen de coincidencias literales; GloVe y FastText
usan posiciones de vectores aprendidas de grandes corpus externos. Además, el
promedio de embeddings descarta el orden de las palabras y el contexto local.
Los archivos FastText usados aquí son vectores precomputados `.vec`, así que no
se infieren palabras ausentes mediante n-gramas; la cobertura medida muestra
que ese límite no afectó a este par. Los puntajes deben interpretarse junto con
la cobertura y el dominio de entrenamiento de cada modelo.
