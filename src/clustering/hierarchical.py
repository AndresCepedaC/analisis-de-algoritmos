"""Clustering jerárquico aglomerativo con tres reglas de enlace."""

from typing import NamedTuple


class Merge(NamedTuple):
    """Una fusión; los nodos iniciales son IDs 0..n-1 y luego n+i."""

    left: int
    right: int
    distance: float
    size: int


METODOS = ("single", "complete", "average")


def _clave(par_a, par_b):
    return (par_a, par_b) if par_a < par_b else (par_b, par_a)


def clustering_jerarquico(matriz_distancias, metodo):
    """Genera las n-1 fusiones usando distancias de enlace desde cero.

    La matriz de distancias entre clusters se actualiza con Lance-Williams:
    single=min, complete=max y average=media ponderada por tamaños.
    """
    if metodo not in METODOS:
        raise ValueError(f"Método no reconocido: {metodo}. Opciones: {METODOS}")

    cantidad = len(matriz_distancias)
    if cantidad < 2 or any(len(fila) != cantidad for fila in matriz_distancias):
        raise ValueError("La matriz de distancias debe ser cuadrada y tener tamaño >= 2.")

    distancias = {}
    for i in range(cantidad):
        for j in range(i + 1, cantidad):
            distancia = float(matriz_distancias[i][j])
            if distancia < 0:
                raise ValueError("Las distancias no pueden ser negativas.")
            distancias[(i, j)] = distancia

    activos = list(range(cantidad))
    tamanos = {identificador: 1 for identificador in activos}
    fusiones = []

    while len(activos) > 1:
        mejor = min(
            (distancias[_clave(a, b)], min(a, b), max(a, b))
            for posicion, a in enumerate(activos)
            for b in activos[posicion + 1:]
        )
        distancia_fusion, izquierda, derecha = mejor
        nuevo = cantidad + len(fusiones)
        tamano_nuevo = tamanos[izquierda] + tamanos[derecha]
        fusiones.append(Merge(izquierda, derecha, distancia_fusion, tamano_nuevo))

        otros = [identificador for identificador in activos if identificador not in (izquierda, derecha)]
        actualizaciones = {}
        for otro in otros:
            distancia_izquierda = distancias[_clave(izquierda, otro)]
            distancia_derecha = distancias[_clave(derecha, otro)]
            if metodo == "single":
                nueva_distancia = min(distancia_izquierda, distancia_derecha)
            elif metodo == "complete":
                nueva_distancia = max(distancia_izquierda, distancia_derecha)
            else:
                nueva_distancia = (
                    tamanos[izquierda] * distancia_izquierda
                    + tamanos[derecha] * distancia_derecha
                ) / tamano_nuevo
            actualizaciones[_clave(nuevo, otro)] = nueva_distancia

        distancias.update(actualizaciones)
        tamanos[nuevo] = tamano_nuevo
        activos = sorted(otros + [nuevo])

    return fusiones


def cortar_arbol(cantidad_hojas, fusiones, cantidad_grupos):
    """Corta el árbol después de n-k fusiones y devuelve una etiqueta por hoja."""
    if not 1 <= cantidad_grupos <= cantidad_hojas:
        raise ValueError("La cantidad de grupos debe estar entre 1 y el número de hojas.")

    clusters = {indice: [indice] for indice in range(cantidad_hojas)}
    for indice_fusion, fusion in enumerate(fusiones[:cantidad_hojas - cantidad_grupos]):
        hojas_izquierda = clusters.pop(fusion.left)
        hojas_derecha = clusters.pop(fusion.right)
        clusters[cantidad_hojas + indice_fusion] = hojas_izquierda + hojas_derecha

    etiquetas = [None] * cantidad_hojas
    for etiqueta, hojas in enumerate(clusters.values()):
        for hoja in hojas:
            etiquetas[hoja] = etiqueta
    return etiquetas
