"""Métricas internas de evaluación para etiquetas y distancias precomputadas."""


def silhouette_promedio(matriz_distancias, etiquetas):
    """Calcula el coeficiente silhouette promedio desde la matriz de distancias."""
    cantidad = len(matriz_distancias)
    if len(etiquetas) != cantidad:
        raise ValueError("Debe existir una etiqueta por elemento de la matriz.")

    grupos = {}
    for indice, etiqueta in enumerate(etiquetas):
        grupos.setdefault(etiqueta, []).append(indice)
    if len(grupos) < 2 or len(grupos) >= cantidad:
        raise ValueError("Silhouette requiere entre 2 y n-1 grupos.")

    siluetas = []
    for indice, etiqueta in enumerate(etiquetas):
        grupo_propio = grupos[etiqueta]
        if len(grupo_propio) == 1:
            siluetas.append(0.0)
            continue

        distancia_interna = sum(
            matriz_distancias[indice][otro]
            for otro in grupo_propio
            if otro != indice
        ) / (len(grupo_propio) - 1)

        distancia_otro_grupo = min(
            sum(matriz_distancias[indice][otro] for otro in grupo)
            / len(grupo)
            for otra_etiqueta, grupo in grupos.items()
            if otra_etiqueta != etiqueta
        )

        denominador = max(distancia_interna, distancia_otro_grupo)
        siluetas.append(
            0.0
            if denominador == 0
            else (distancia_otro_grupo - distancia_interna) / denominador
        )

    return sum(siluetas) / cantidad
