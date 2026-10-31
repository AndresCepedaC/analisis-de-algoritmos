"""Representación del árbol de fusiones con Matplotlib."""

from pathlib import Path

import matplotlib.pyplot as plt


def guardar_dendrograma(articulos, ids, fusiones, metodo, ruta_salida):
    """Dibuja un dendrograma a partir de las fusiones propias del proyecto."""
    cantidad = len(ids)
    posiciones = {indice: float(indice) for indice in range(cantidad)}
    alturas = {indice: 0.0 for indice in range(cantidad)}
    figura, eje = plt.subplots(figsize=(13, 6))

    for indice_fusion, fusion in enumerate(fusiones):
        x_izquierda = posiciones[fusion.left]
        x_derecha = posiciones[fusion.right]
        y_izquierda = alturas[fusion.left]
        y_derecha = alturas[fusion.right]
        altura = fusion.distance

        eje.plot([x_izquierda, x_izquierda], [y_izquierda, altura], color="#345995", linewidth=1.2)
        eje.plot([x_derecha, x_derecha], [y_derecha, altura], color="#345995", linewidth=1.2)
        eje.plot([x_izquierda, x_derecha], [altura, altura], color="#345995", linewidth=1.2)

        nuevo = cantidad + indice_fusion
        posiciones[nuevo] = (x_izquierda + x_derecha) / 2
        alturas[nuevo] = altura

    etiquetas = [f"{identificador:02d}" for identificador in ids]
    eje.set_xticks(range(cantidad), etiquetas, fontsize=8)
    eje.set_xlabel("ID del artículo (ver agrupaciones_mejores.csv)")
    eje.set_ylabel("Distancia coseno TF-IDF")
    eje.set_title(f"Clustering jerárquico · {metodo.title()} linkage")
    eje.grid(axis="y", alpha=0.2)
    figura.tight_layout()

    ruta_salida = Path(ruta_salida)
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)
    figura.savefig(ruta_salida, dpi=180, bbox_inches="tight")
    plt.close(figura)
