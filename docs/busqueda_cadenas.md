# Requerimiento 3: búsqueda exacta de cadenas

## Entrada y resultados

La búsqueda se aplica al abstract original conservado en `data/corpus_articulos.csv`.
Es exacta y sensible a mayúsculas: se buscan las mismas letras, espacios y
signos que escriba el usuario. Los índices internos comienzan en cero; los CSV
reportan posiciones de carácter comenzando en uno.

```powershell
python main.py busqueda --patron "AI" --repeticiones 7
```

También se puede omitir `--patron` y escribirlo en la consola. Los archivos se
guardan en `output/searching/`: `ocurrencias.csv` contiene artículo, cantidad y
posiciones; `rendimiento.csv` separa el tiempo de preprocesamiento y el tiempo
de búsqueda, además de comparaciones y colisiones de hash. Por defecto se
realizan siete repeticiones y se informa la mediana de los tiempos; se puede
ajustar con `--repeticiones`.

## Algoritmos implementados

Los tres algoritmos están en `src/searching/algorithms.py`; no se usa `find`,
`index` ni una biblioteca que implemente búsqueda de patrones.

### Knuth-Morris-Pratt (KMP)

`preparar_kmp` construye LPS, el prefijo propio más largo que también es sufijo
para cada prefijo del patrón. Cuando hay un desacuerdo, el texto no retrocede:
el patrón se alinea con el prefijo que aún puede coincidir.

- Preparación: `O(m)` tiempo y `O(m)` espacio.
- Búsqueda: `O(n)` tiempo en el texto, ya que cada carácter del texto avanza como
  máximo una vez; espacio adicional `O(1)` durante el recorrido.

### Boyer-Moore, regla del carácter malo

`preparar_boyer_moore` guarda el índice de la última aparición de cada carácter
del patrón. La comparación comienza por el extremo derecho. Si el carácter del
texto `c` no coincide con el carácter `j` del patrón, el desplazamiento es:

```text
desplazamiento = max(1, j - última_aparición(c))
```

El patrón se desplaza al menos una posición después de una coincidencia para
conservar matches solapados. Esta versión usa la regla del carácter malo; no
añade la tabla de sufijo bueno.

- Preparación: `O(m)` tiempo y hasta `O(min(m, σ))` espacio, donde `σ` es el
  alfabeto observado en el patrón.
- Búsqueda: mejor caso sublineal al saltar varias posiciones por desacuerdo;
  peor caso `O(nm)` para esta versión simplificada.

### Rabin-Karp

Se usa un hash polinómico con base `256` y módulo `1 000 000 007`. El hash de la
primera ventana se calcula una vez. Al avanzar una posición se quita el carácter
saliente, se desplaza el hash y se añade el carácter entrante:

```text
H_nueva = (base × (H_actual - valor_saliente × base^(m-1))
           + valor_entrante) mod q
```

Si los hashes coinciden se comparan los caracteres antes de reportar el match;
así una colisión no produce un falso positivo.

- Preparación del patrón: `O(m)` tiempo.
- Búsqueda esperada: `O(n+m)`; peor caso `O(nm)` si muchos hashes colisionan.
- Espacio auxiliar: `O(1)` aparte de las posiciones encontradas.

Aquí `n` es la longitud del texto, `m` la del patrón y `σ` el número de
caracteres distintos posibles. En el corpus completo, `n` representa la suma
de longitudes de los abstracts procesados. El CLI mide por separado la
preparación de cada patrón y su búsqueda en todos los abstracts; informa la
mediana de las repeticiones para reducir el efecto de variaciones puntuales del
sistema. Los tiempos dependen del equipo y el patrón.

## Caso de estudio

El patrón de demostración es `AI` en el abstract 1, **Artificial intelligence
literacy in higher and adult education: A scoping literature review**. El
fragmento de texto utilizado es:

> Since artificial intelligence (AI) is finding its way into more and more areas of everyday life, improving the AI skills of non-experts is important and will become even more relevant in the future.

KMP construye LPS `[0, 0]`: ningún prefijo propio no vacío de `AI` coincide con
un sufijo. Boyer-Moore prepara la tabla de última aparición `{A: 0, I: 1}` y
compara primero el carácter `I` desde la derecha. Rabin-Karp calcula el hash:

```text
H("AI") = (256 × ord("A") + ord("I")) mod 1 000 000 007
         = (256 × 65 + 73) mod 1 000 000 007
         = 16 713
```

Para `AI`, los tres algoritmos encontraron 143 ocurrencias en el corpus y
coincidieron en todas las posiciones. En el abstract 1 reportaron siete
apariciones, en las posiciones (base uno) `32, 112, 271, 381, 391, 512, 981`.
Por ejemplo, en la primera coincidencia el segmento `AI` ocupa los índices
internos 31–32, que se reportan como posición 32.

### Traza breve

En el inicio del fragmento citado, Boyer-Moore compara `I` con la `i` minúscula
del final de `Si`. Como no coinciden y la `i` minúscula no está en el patrón,
desplaza dos posiciones. En el índice interno 30, la ventana es `(A`; falla al
comparar `I` con `A` y desplaza una posición porque `A` aparece en el patrón en
el índice 0. En el índice 31 encuentra `AI` y reporta la posición 32. KMP llega
a la misma coincidencia avanzando el texto y usando LPS `[0, 0]` ante desacuerdos.
Rabin-Karp calcula `H("Si") = 21 353`, actualiza el hash al deslizar la ventana,
y solo verifica carácter por carácter las ventanas cuyo hash es `16 713`; las
coincidencias se confirman exactamente.

### Medición observada

Se midió la búsqueda en los 20 abstracts, con siete repeticiones; se muestran
medianas de milisegundos. Las comparaciones de caracteres cuentan actividades
distintas por algoritmo: KMP y Boyer-Moore cuentan sus comparaciones durante
el recorrido, mientras Rabin-Karp cuenta las verificaciones carácter a carácter
de las ventanas con hash coincidente.

| Algoritmo | Preparación (ms) | Búsqueda (ms) | Comparaciones de caracteres | Colisiones | Coincidencias |
| --- | ---: | ---: | ---: | ---: | ---: |
| KMP | 0.0033 | 2.7359 | 28 475 | 0 | 143 |
| Boyer-Moore | 0.0023 | 3.2135 | 14 487 | 0 | 143 |
| Rabin-Karp | 0.0060 | 6.2049 | 286 | 0 | 143 |

En esta ejecución Rabin-Karp hizo menos verificaciones directas de caracteres,
pero tardó más debido al costo de calcular y actualizar hashes en Python para
cada ventana. Este resultado puntual ilustra que el número de comparaciones y
el tiempo de ejecución no son equivalentes; no altera las cotas teóricas ni
permite generalizar el rendimiento a otros patrones, corpus o equipos. El CSV
generado contiene los valores con mayor precisión.
