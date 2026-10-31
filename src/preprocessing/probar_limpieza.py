
from limpieza_texto import normalizar_texto


texto_prueba = """
Artificial Intelligence (AI) is transform-
ing education. AI supports learning!
"""

resultado = normalizar_texto(texto_prueba)

print("Texto original:")
print(texto_prueba)

print("\nTexto normalizado:")
print(resultado)
