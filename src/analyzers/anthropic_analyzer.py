"""
Este módulo contiene funciones específicas para analizar texto con modelos de Anthropic (Claude).
¡Ojo! La forma exacta de tokenizar y los precios pueden requerir información actualizada
de la API de Anthropic. Este es un esquema inicial.

Anthropic utiliza su propio tokenizador. No hay una librería pública oficial de Python
tan directa como `tiktoken` para sus modelos más recientes (Claude 3).
Para modelos anteriores (Claude 2, etc.), se podría usar la librería `anthropic`.
Sin embargo, para Claude 3, la documentación sugiere usar la API para contar tokens.
Como alternativa local, podemos usar una aproximación basada en la librería `tiktoken`
ya que algunos modelos de Anthropic tienen codificaciones similares.

"""
#librerias

import tiktoken
import json

def contar_tokens_anthropic(texto, modelo):
    """
    Esata función intenta contar el número de tokens para modelos de Anthropic.
    Para Claude 3, esto es una APROXIMACIÓN basada en codificaciones similares.
    Para modelos anteriores, podría requerir la librería `anthropic` o una codificación específica.

    Args:
        texto (str): El texto para tokenizar.
        modelo (str): El nombre del modelo de Anthropic (ej. "Claude 3 Opus", "Claude 3 Sonnet").

    Returns:
        int: Una estimación del número de tokens.
    """
    try:
        if "claude-3" in modelo.lower():
            # Claude 3 utiliza una codificación similar a cl100k_base
            encoding = tiktoken.get_encoding("cl100k_base")
        elif "claude-2" in modelo.lower():
            # Claude 2 podría usar una codificación diferente
            # Esto es una suposición y podría no ser exacto
            encoding = tiktoken.get_encoding("oa2")
        else:
            # Intenta con una codificación genérica
            encoding = tiktoken.get_encoding("utf-8")
        return len(encoding.encode(texto))
    except KeyError:
        return int(len(texto.split()) * 0.8) if texto else 0 # Último recurso: estimación por palabras

def calcular_costo_anthropic(tokens_entrada, tokens_salida, modelo, precios_modelos, moneda="USD"):
    """
    Esta función calcula el costo estimado de tokens de entrada y salida para un modelo de Anthropic.
    Los precios aquí son EJEMPLOS y deben ser verificados con la información actual de Anthropic.

    Args:
        tokens_entrada (int): Número de tokens en el prompt de entrada.
        tokens_salida (int): Número de tokens en la salida generada.
        modelo (str): Nombre del modelo de Anthropic (ej. "Claude 3 Opus", "Claude 3 Sonnet").
        precios_modelos (dict): Diccionario con las tarifas por 1000 tokens para cada modelo de Anthropic.
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
    precios_anthropic_ejemplo = {
        "Claude 3 Opus": {"entrada": 0.015, "salida": 0.075},
        "Claude 3 Sonnet": {"entrada": 0.003, "salida": 0.015},
        "Claude 3 Haiku": {"entrada": 0.00025, "salida": 0.00125},
    }

    texto_entrada_claude = "¿Qué tres cosas son necesarias para sobrevivir?"
    texto_salida_claude_opus = "Tres cosas necesarias para sobrevivir son agua, comida y refugio."
    texto_salida_claude_sonnet = "Para la supervivencia se requieren elementos esenciales como agua, alimento y un lugar seguro para resguardarse."

    modelo_opus = "Claude 3 Opus"
    tokens_entrada_opus = contar_tokens_anthropic(texto_entrada_claude, modelo_opus)
    tokens_salida_opus = contar_tokens_anthropic(texto_salida_claude_opus, modelo_opus)
    costos_opus = calcular_costo_anthropic(tokens_entrada_opus, tokens_salida_opus, modelo_opus, precios_anthropic_ejemplo, "USD")

    print(f"Modelo: {modelo_opus}")
    print(f"  Tokens Entrada (estimado): {tokens_entrada_opus}")
    print(f"  Tokens Salida (estimado): {tokens_salida_opus}")
    print(f"  Costos (USD): {costos_opus}")

    modelo_sonnet = "Claude 3 Sonnet"
    tokens_entrada_sonnet = contar_tokens_anthropic(texto_entrada_claude, modelo_sonnet)
    tokens_salida_sonnet = contar_tokens_anthropic(texto_salida_claude_sonnet, modelo_sonnet)
    costos_sonnet = calcular_costo_anthropic(tokens_entrada_sonnet, tokens_salida_sonnet, modelo_sonnet, precios_anthropic_ejemplo, "EUR")

    print(f"\nModelo: {modelo_sonnet}")
    print(f"  Tokens Entrada (estimado): {tokens_entrada_sonnet}")
    print(f"  Tokens Salida (estimado): {tokens_salida_sonnet}")
    print(f"  Costos (EUR): {costos_sonnet}")

    modelo_haiku = "Claude 3 Haiku"
    tokens_entrada_haiku = contar_tokens_anthropic(texto_entrada_claude, modelo_haiku)
    tokens_salida_haiku = contar_tokens_anthropic(texto_salida_claude_opus, modelo_haiku) # Usando la misma salida para comparar
    costos_haiku = calcular_costo_anthropic(tokens_entrada_haiku, tokens_salida_haiku, modelo_haiku, precios_anthropic_ejemplo, "USD")

    print(f"\nModelo: {modelo_haiku}")
    print(f"  Tokens Entrada (estimado): {tokens_entrada_haiku}")
    print(f"  Tokens Salida (estimado): {tokens_salida_haiku}")
    print(f"  Costos (USD): {costos_haiku}")

    modelo_no_existente_anthropic = "Claude-Modelo-Inventado"
    costos_no_existente_anthropic = calcular_costo_anthropic(100, 50, modelo_no_existente_anthropic, precios_anthropic_ejemplo)
    print(f"\nModelo: {modelo_no_existente_anthropic}, Costos: {costos_no_existente_anthropic}")
"""
NOTA IMPORTANTE: Para una implementación precisa con modelos de Anthropic,
se recomienda utilizar la API de Anthropic y su funcionalidad para contar tokens.
Las aproximaciones locales pueden no ser exactas, especialmente para los modelos Claude 3.
"""