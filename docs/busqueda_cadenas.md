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

Para hacer explícito el cálculo rolling de esa primera ventana:

```text
H("Si") = (256 × 83 + 105) mod q = 21 353
H("in") = (256 × (21 353 - 83 × 256) + 110) mod q
         = (256 × 105 + 110) mod q = 26 990
```

El siguiente paso sigue la misma actualización, quitando el primer carácter
de la ventana anterior y añadiendo el carácter que entra. Cuando una ventana
produce el hash `16 713`, el algoritmo comprueba sus caracteres contra `AI`;
solo si ambos coinciden registra la posición. En esta ejecución no se observaron
colisiones (`colisiones_hash = 0`); la verificación sigue siendo necesaria
porque la función modular, en general, puede asignar el mismo hash a cadenas
distintas.

La tabla de Boyer-Moore se construye de izquierda a derecha: `A` se registra en
0 y `I` en 1, dando `{A: 0, I: 1}`. Sus primeras alineaciones muestran la
heurística y los saltos:

| Inicio interno | Ventana | Comparación desde la derecha | Carácter malo | Desplazamiento | Resultado |
| ---: | --- | --- | --- | ---: | --- |
| 0 | `Si` | `I ≠ i` | `i` (ausente, última = -1) | 2 | desacuerdo |
| 30 | `(A` | `I ≠ A` | `A` (última = 0) | 1 | desacuerdo |
| 31 | `AI` | `I = I`, luego `A = A` | — | 1 | coincidencia, posición 32 |

KMP primero calcula LPS `[0,0]`: en el patrón de dos caracteres no existe
prefijo propio no vacío que también sea sufijo. Durante la búsqueda, cada
desacuerdo con el primer carácter deja el índice del patrón en cero y avanza el
índice del texto; al reconocer `AI`, emite el inicio y restaura el índice del
patrón al último valor LPS (cero), lo que permite seguir buscando coincidencias.

En esta primera coincidencia, el recorrido de KMP puede resumirse sin omitir
ningún tramo: para cada índice de texto `0..30`, compara el carácter con `A`,
falla con `j=0` y avanza el índice del texto una posición. En el índice 31,
`A=A` avanza el patrón a `j=1`; en el índice 32, `I=I` completa el patrón y
reporta el inicio 31 (posición 32). Como `LPS[1]=0`, el siguiente intento
comienza con el patrón desde su primer carácter.

Rabin-Karp calcula inicialmente `H("Si")=21 353`. La tabla muestra todos los
hashes hasta la primera coincidencia; cada fila posterior se obtiene de la
anterior con la fórmula rolling, no recalculando la cadena desde cero:

| Inicio | Ventana | Hash | Inicio | Ventana | Hash |
| ---: | --- | ---: | ---: | --- | ---: |
| 0 | `Si` | 21 353 | 16 | ` i` | 8 297 |
| 1 | `in` | 26 990 | 17 | `in` | 26 990 |
| 2 | `nc` | 28 259 | 18 | `nt` | 28 276 |
| 3 | `ce` | 25 445 | 19 | `te` | 29 797 |
| 4 | `e ` | 25 888 | 20 | `el` | 25 964 |
| 5 | ` a` | 8 289 | 21 | `ll` | 27 756 |
| 6 | `ar` | 24 946 | 22 | `li` | 27 753 |
| 7 | `rt` | 29 300 | 23 | `ig` | 26 983 |
| 8 | `ti` | 29 801 | 24 | `ge` | 26 469 |
| 9 | `if` | 26 982 | 25 | `en` | 25 966 |
| 10 | `fi` | 26 217 | 26 | `nc` | 28 259 |
| 11 | `ic` | 26 979 | 27 | `ce` | 25 445 |
| 12 | `ci` | 25 449 | 28 | `e ` | 25 888 |
| 13 | `ia` | 26 977 | 29 | ` (` | 8 232 |
| 14 | `al` | 24 940 | 30 | `(A` | 10 305 |
| 15 | `l ` | 27 680 | 31 | `AI` | 16 713 |

Solo en el inicio 31 el hash de ventana coincide con el hash del patrón. Se
verifican entonces los caracteres (`A=A`, `I=I`) y se reporta la posición. En
estas 32 ventanas no hubo colisión; para cualquier coincidencia de hash, la
verificación explícita previene reportar falsos positivos.

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
