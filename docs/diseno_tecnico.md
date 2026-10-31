# Diseño técnico y arquitectura

## Alcance

El proyecto procesa los abstracts de 20 archivos PDF del corpus estático
entregado para la asignatura. Los títulos y autores se conservan para mostrar
los resultados y cruzarlos con los identificadores. La aplicación se ejecuta
localmente desde consola con Python; no se ha publicado un servicio web ni una
instancia remota.

## Arquitectura

```text
PDFs del corpus
      │ extracción
      ▼
data/corpus_articulos.csv ───────────────┐
      │                                   │
      ├── normalización ── similitud      ├── búsqueda exacta sobre abstract original
      │                   (R1)            │   KMP / Boyer-Moore / Rabin-Karp (R3)
      │                                   │
      └── TF-IDF ── distancia coseno      │
                   └─ clustering (R2)     │
                                          ▼
                         CSV, dendrogramas y documentación
```

El punto de entrada `main.py` despacha los comandos a interfaces CLI separadas.
Cada módulo separa algoritmos, servicios de cálculo y escritura de resultados:

| Componente | Responsabilidad |
| --- | --- |
| `src/extraction/` | Extraer abstract, título y autores de los PDF y generar el corpus tabular. |
| `src/preprocessing/` | Normalizar abstracts para las tareas que comparan contenido. |
| `src/similarity/` | Cargar corpus, ejecutar cuatro medidas clásicas y dos medidas basadas en embeddings. |
| `src/clustering/` | Construir desde cero los tres enlaces, evaluar silhouette y dibujar dendrogramas. |
| `src/searching/` | Buscar patrones exactos sobre el abstract original y medir algoritmos. |
| `app.py` | Interfaz web Streamlit que presenta los tres requerimientos y reutiliza los servicios. |
| `data/` | Corpus y resultados de similitud. Los modelos grandes quedan locales e ignorados por Git. |
| `output/` | Resultados reproducibles de clustering y búsqueda. |
| `docs/` | Método, análisis, casos de estudio, decisiones y limitaciones. |

## Decisiones de procesamiento

- Similitud y clustering usan el abstract normalizado; similitud conserva
  frecuencia/ponderación según cada medida y clustering usa TF-IDF con distancia
  coseno.
- La búsqueda exacta usa el abstract original para preservar capitalización,
  signos y posiciones, y no altera los datos antes de buscar.
- GloVe y FastText se cargan desde archivos locales preentrenados. No se entrena
  un modelo nuevo con un corpus de solo 20 documentos.
- Las dependencias de ejecución declaradas están en `requirements.txt`.

## Ejecución local

Desde la raíz del repositorio, instalar dependencias y ejecutar, por ejemplo:

```powershell
python -m pip install -r requirements.txt
python main.py --ids 1 10 --salida data/resultados_similitud_1_10.csv
python main.py clustering
python main.py busqueda --patron "AI"
python -m streamlit run app.py
```

La similitud con embeddings requiere además los dos archivos descritos en
`modelos_embeddings.md`. El comando actual es una ejecución local: para afirmar
que el proyecto está desplegado se debe elegir y completar el destino requerido
(por ejemplo, paquete ejecutable, servidor institucional o plataforma web) y
registrar su URL o instrucciones de acceso. El PDF no especifica plataforma ni
modalidad concreta de despliegue.

## Declaración de apoyo de IA generativa

Durante el desarrollo se utilizó ChatGPT/Codex como herramienta de apoyo para
organizar la arquitectura, redactar documentación, proponer y revisar código,
analizar salidas y corregir errores. Las implementaciones de los algoritmos
solicitados están expresadas explícitamente en el código del proyecto; la
herramienta no sustituye la explicación matemática, la interpretación de los
resultados ni la validación académica que corresponde al equipo. Esta
declaración debe ajustarse si otros integrantes utilizaron herramientas
adicionales y revisarse frente al documento complementario del docente sobre
uso de IA, si fue suministrado.

## Mapa de documentación

- Requerimiento 1: `similitud_textual.md`, `caso_estudio_similitud.md`,
  `modelos_embeddings.md`.
- Requerimiento 2: `clustering_jerarquico.md`.
- Requerimiento 3: `busqueda_cadenas.md`.
- Interfaz/despliegue: `despliegue_streamlit.md`.
- Corpus y extracción: `corpus_y_normalizacion.md`.
