# Interfaz y despliegue con Streamlit Community Cloud

## Aplicación web

`app.py` es el punto de entrada de la interfaz Streamlit. Reutiliza los módulos
del proyecto para ofrecer tres vistas:

- **Similitud:** seleccionar artículos y ejecutar las cuatro medidas clásicas;
  permite incluir GloVe/FastText si los archivos están disponibles en el
  entorno.
- **Clustering:** ejecutar los tres enlaces, consultar silhouette, ver los
  dendrogramas y revisar el mejor corte.
- **Búsqueda:** ingresar un patrón, comparar KMP/Boyer-Moore/Rabin-Karp y
  descargar las posiciones encontradas.

No se crea un proyecto o repositorio paralelo. La interfaz y el CLI llaman a
los mismos servicios y algoritmos existentes.

## Ejecutar localmente

Desde la raíz del repositorio:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

El catálogo `data/corpus_articulos.csv` debe estar presente. Si se desean
incluir las medidas de embeddings en ejecución local, los archivos de modelos
deben estar en `data/models/` (o se puede definir `EMBEDDINGS_DIR`). Son
opcionales para la interfaz y permanecen excluidos de Git.

## Publicar en Streamlit Community Cloud

1. Subir el repositorio del proyecto a GitHub. Incluir `app.py`, `src/`,
   `data/corpus_articulos.csv`, `requirements.txt` y `.streamlit/config.toml`.
2. Abrir Streamlit Community Cloud y conectar la cuenta de GitHub.
3. Crear una aplicación nueva, seleccionar repositorio y rama, y establecer
   `app.py` como archivo principal.
4. En **Advanced settings**, elegir Python 3.12 (versión predeterminada actual
   de Community Cloud) y dejar los secretos vacíos; esta app no usa secretos.
5. Pulsar **Deploy** y abrir la URL generada bajo `streamlit.app`.

La aplicación detecta si el CSV no está incluido y muestra un mensaje directo.
No subir los PDF originales ni los modelos pesados al repositorio por esta
configuración. En Cloud, los resultados de embeddings quedan deshabilitados si
los dos archivos no se proporcionan en el entorno. GloVe ocupa unos 69 MB y el
archivo FastText usado en el caso de estudio ronda 1 GB; cargar FastText puede
superar los recursos del plan gratuito o provocar arranques lentos. La
comparación clásica, el clustering y la búsqueda no dependen de esos archivos.

Streamlit Community Cloud duerme apps inactivas y aplica límites de recursos
que pueden cambiar. La publicación pública también hace accesible la
información que la aplicación muestra; confirmar con el equipo que el corpus
puede compartirse antes de habilitar una URL pública.

## Lo que esta configuración no hace

La configuración prepara la app para que el titular de la cuenta la publique;
no crea una cuenta de Streamlit, no sube el repositorio a GitHub y no publica
la aplicación por sí misma. Tras el despliegue, registrar la URL final en el
README y en el documento de entrega. La secuencia de configuración coincide
con la [guía oficial de despliegue](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy).
