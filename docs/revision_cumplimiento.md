# Revisión de cumplimiento frente al PDF del proyecto

Revisión del archivo de consignas entregado para el proyecto, contrastada con
el código, la configuración, la documentación y los resultados presentes en el
repositorio al 31 de octubre de 2026. “Cumple” indica evidencia implementada;
“parcial” señala una brecha que todavía impide afirmar cumplimiento total.

| Requerimiento | Estado | Evidencia en el proyecto | Pendiente o límite |
| --- | --- | --- | --- |
| 1. Similitud textual | **Cumple** | CLI permite seleccionar dos o más IDs; cuatro medidas explícitas (Levenshtein, coseno TF-IDF, Jaccard, Dice); GloVe y FastText; resultados para artículos 1 y 10 en `data/resultados_similitud_1_10.csv`; comparación crítica y cálculos numéricos de todos los métodos en `caso_estudio_similitud.md`. | Los modelos preentrenados permanecen fuera de Git por tamaño/licencia; se documentan descarga, versión y licencias. Para reproducir los dos resultados IA, cada equipo debe tener los archivos locales. |
| 2. Clustering jerárquico | **Cumple en implementación y análisis** | Tres enlaces implementados desde cero; dendrogramas para los 20 abstracts; evaluación de cortes mediante silhouette; puntuaciones, fusiones y grupos exportados en `output/clustering/`; método y lectura crítica en `clustering_jerarquico.md`. | Los tres enlaces empatan con silhouette `0.103132`, una separación débil; se reporta ese resultado sin escoger artificialmente un ganador. |
| 3. Búsqueda exacta | **Cumple** | KMP, Boyer-Moore (carácter malo) y Rabin-Karp implementados explícitamente; la búsqueda de `AI` coincide en los tres métodos sobre los 20 abstracts; posiciones y mediciones en `output/searching/`; no se usan `find()` ni `index()` en `src/searching/`. | La demostración usa `AI`, que es un patrón representativo del corpus; no se observaron colisiones en el caso empírico y se explica cómo la verificación evita falsos positivos. |
| 4. Despliegue y documentación técnica | **Interfaz preparada; despliegue pendiente** | Guías para los requerimientos 1–3, arquitectura y declaración de uso de IA; aplicación Streamlit en `app.py`; instrucciones de despliegue en `despliegue_streamlit.md`. | La URL todavía no existe: hay que publicar desde una cuenta GitHub/Streamlit. La demo en Cloud no carga los modelos grandes ignorados por Git; las medidas con embeddings requieren que esos archivos estén disponibles en el entorno. El documento técnico está en Markdown y aún requiere consolidación/formato de entrega si el curso exige un informe final separado. |

## Revisión por criterio

### Requerimiento 1

- Selección dinámica de dos o más artículos: presente (`src/similarity/cli.py`).
- Cuatro métodos clásicos: presentes en `src/similarity/classic.py`.
- Dos métodos con embeddings: presentes mediante vectores GloVe y FastText
  preentrenados en `src/similarity/embeddings.py`; origen, licencias, cobertura
  y limitaciones están descritos en `modelos_embeddings.md`.
- Caso práctico e interpretación: presentes para artículos 1 y 10.
- Caso de estudio: documenta el promedio de vectores, cobertura de vocabulario,
  dimensiones, primeras coordenadas, productos punto, normas y cosenos para
  GloVe y FastText en el mismo par. El modelo no se interpreta como entrenado
  con los 20 abstracts.

### Requerimiento 2

- Se usan 20 abstracts normalizados, TF-IDF y distancia coseno.
- Single, complete y average linkage son explícitos y actualizan distancias con
  sus fórmulas; no se delega a una biblioteca de clustering.
- Se generan tres dendrogramas y se elige el mejor corte con silhouette.
- El resultado actual es empate y bajo: `k=2`, silhouette `0.103132` para cada
  enlace. La documentación explica la limitación interpretativa.

### Requerimiento 3

- La cadena la ingresa el usuario y se busca literalmente sobre el abstract
  original de cada documento.
- Los tres algoritmos están implementados desde cero sin funciones nativas de
  búsqueda de subcadenas.
- El caso actual muestra patrón `AI`, posiciones, todos los alineamientos de
  Boyer-Moore hasta la primera coincidencia, recorrido KMP hasta el primer
  match, hashes rolling de Rabin-Karp y medianas medidas en siete repeticiones.
- La evaluación crítica debe conservar el contexto: el tiempo observado depende
  del intérprete, el corpus y el patrón; la cuenta de comparaciones de
  Rabin-Karp solo incluye verificación de ventanas con hash coincidente.

### Requerimiento 4

- Documentación por módulo y arquitectura: presente en Markdown.
- Declaración de uso de IA generativa: incorporada; los integrantes deben
  confirmar si usaron herramientas adicionales y alinearla con cualquier guía
  adicional del docente.
- Despliegue: la interfaz y las instrucciones para Cloud están preparadas, pero
  no hay publicación ni URL todavía. Además, la demo alojada no calcula
  embeddings sin disponer de los archivos locales de modelo.

## Conclusión

Los requerimientos 1–3 cuentan ahora con implementación y evidencia documental
para el alcance descrito. No es correcto declarar que todo el proyecto ya
cumple completamente: falta definir y realizar el despliegue, y consolidar el
documento final en el formato que solicite el curso.
