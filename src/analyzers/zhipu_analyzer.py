"""
Este módulo contendrá funciones específicas para analizar texto con modelos de Zhipu AI (GLM).
¡Ojo! La forma exacta de tokenizar y los precios pueden requerir información actualizada
de la API de Zhipu AI Open Platform. Este es un esquema inicial.

Zhipu AI tiene su propia API y documentación sobre cómo tokenizar.
Podemos intentar usar la librería `tiktoken` con la codificación `chatglm2` o `glm-4`
ya que algunos modelos GLM se basan en arquitecturas Transformer similares.
alternativamente, podríamos necesitar interactuar directamente con la API de Zhipu
para obtener un conteo preciso de tokens.

"""
#librerias

import tiktoken
import json

def contar_tokens_zhipu(texto, modelo):
    """
    Esta función intenta contar el número de tokens para modelos de Zhipu AI (GLM).
    Esto es una APROXIMACIÓN basada en codificaciones similares disponibles en `tiktoken`.
    Para un conteo preciso, se recomienda usar la API de Zhipu AI.

    Args:
        texto (str): El texto para tokenizar.
        modelo (str): El nombre del modelo GLM (ej. "GLM-4", "GLM-4-Long").

    Returns:
        int: Una estimación del número de tokens.
    """
    try:
        if "glm-4" in modelo.lower():
            # GLM-4 podría usar una codificación similar a cl100k_base o una específica
            # Intentamos con cl100k_base como una aproximación
            encoding = tiktoken.get_encoding("cl100k_base")
        elif "chatglm2" in modelo.lower():
            # ChatGLM2 tiene su propia codificación
            encoding = tiktoken.get_encoding("chatglm2")
        else:
            # Intenta con una codificación genérica
            encoding = tiktoken.get_encoding("utf-8")
        return len(encoding.encode(texto))
    except KeyError:
        return int(len(texto.split()) * 0.7) if texto else 0 # Otra estimación basada en palabras

def calcular_costo_zhipu(tokens_entrada, tokens_salida, modelo, precios_modelos, moneda="USD"):
    """
    Esta función calcula el costo estimado de tokens de entrada y salida para un modelo de Zhipu AI (GLM).
    Los precios aquí son EJEMPLOS y deben ser verificados con la información actual de Zhipu AI.

    Args:
        tokens_entrada (int): Número de tokens en el prompt de entrada.
        tokens_salida (int): Número de tokens en la salida generada.
        modelo (str): Nombre del modelo GLM (ej. "GLM-4-Plus", "GLM-4-Long").
        precios_modelos (dict): Diccionario con las tarifas por 1000 tokens para cada modelo GLM.
        moneda (str, opcional): La moneda en la que se mostrará el costo. Por defecto es USD.

    Returns:
        dict: Un diccionario con el costo de entrada, el costo de salida y el costo total estimado,
              formateado con la moneda especificada. Devuelve None si el modelo no se encuentra
              en la estructura de precios.
    """
    if modelo not in precios_modelos:
        return None

    tarifa_entrada = precios_modelos[modelo].get("entrada", 0)
    tarifa_salida = precios_modelos[modelo].get("salida", 0)

    costo_entrada = (tokens_entrada / 1000) * tarifa_entrada
    costo_salida = (tokens_salida / 1000) * tarifa_salida
    costo_total = costo_entrada + costo_salida

    return {
        f"costo_entrada_{moneda}": f"{costo_entrada:.6f}",
        f"costo_salida_{moneda}": f"{costo_salida:.6f}",
        f"costo_total_{moneda}": f"{costo_total:.6f}"
    }

if __name__ == "__main__":
    # Ejemplo de uso (esto no se ejecutará cuando se importe como módulo)
    precios_zhipu_ejemplo = {
        "GLM-4-Plus": {"entrada": 0.0007, "salida": 0.0007},
        "GLM-4-Long": {"entrada": 0.00014, "salida": 0.00014},
        "GLM-4-AirX": {"entrada": 0.0014, "salida": 0.0014},
    }

    texto_entrada_glm = "¿Cuál es la capital de China?"
    texto_salida_glm = "中国的首都是北京。"

    modelo_glm_plus = "GLM-4-Plus"
    tokens_entrada_glm_plus = contar_tokens_zhipu(texto_entrada_glm, modelo_glm_plus)
    tokens_salida_glm_plus = contar_tokens_zhipu(texto_salida_glm, modelo_glm_plus)
    costos_glm_plus = calcular_costo_zhipu(tokens_entrada_glm_plus, tokens_salida_glm_plus, modelo_glm_plus, precios_zhipu_ejemplo, "USD")

    print(f"Modelo: {modelo_glm_plus}")
    print(f"  Tokens Entrada (estimado): {tokens_entrada_glm_plus}")
    print(f"  Tokens Salida (estimado): {tokens_salida_glm_plus}")
    print(f"  Costos (USD): {costos_glm_plus}")

    modelo_glm_long = "GLM-4-Long"
    tokens_entrada_glm_long = contar_tokens_zhipu(texto_entrada_glm, modelo_glm_long)
    tokens_salida_glm_long = contar_tokens_zhipu(texto_salida_glm, modelo_glm_long)
    costos_glm_long = calcular_costo_zhipu(tokens_entrada_glm_long, tokens_salida_glm_long, modelo_glm_long, precios_zhipu_ejemplo, "EUR")

    print(f"\nModelo: {modelo_glm_long}")
    print(f"  Tokens Entrada (estimado): {tokens_entrada_glm_long}")
    print(f"  Tokens Salida (estimado): {tokens_salida_glm_long}")
    print(f"  Costos (EUR): {costos_glm_long}")

    modelo_no_existente_glm = "GLM-Modelo-Inventado"
    costos_no_existente_glm = calcular_costo_zhipu(100, 50, modelo_no_existente_glm, precios_zhipu_ejemplo)
    print(f"\nModelo: {modelo_no_existente_glm}, Costos: {costos_no_existente_glm}")
"""
NOTA IMPORTANTE: Para una implementación precisa con modelos de Zhipu AI,
se recomienda investigar y utilizar la documentación y las herramientas proporcionadas
por la API de Zhipu AI Open Platform para la tokenización y los precios.
Las aproximaciones locales pueden no ser exactas.
"""