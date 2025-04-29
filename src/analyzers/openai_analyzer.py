#librerias
import tiktoken
import json
"""
Esta función toma un texto y un modelo de OpenAI, y devuelve el número de tokens en el texto.
Los modelos de OpenAI tienen diferentes codificaciones, y esta función utiliza la biblioteca tiktoken para determinar el número de tokens en el texto según el modelo especificado.
"""
def contar_tokens_openai(texto, modelo):

    try:
        encoding = tiktoken.encoding_for_model(modelo)
        return len(encoding.encode(texto))
    except KeyError:
        return None

"""
Esta función calcula el costo estimado de tokens de entrada y salida para un modelo de OpenAI.

    Args:
        tokens_entrada (int): Número de tokens en el prompt de entrada.
        tokens_salida (int): Número de tokens en la salida generada.
        modelo (str): Nombre del modelo de OpenAI.
        precios_modelos (dict): Diccionario con las tarifas por 1000 tokens para cada modelo.
        moneda (str, opcional): La moneda en la que se mostrará el costo. Por defecto es USD.

    Returns:
        dict: Un diccionario con el costo de entrada, el costo de salida y el costo total estimado,
              formateado con la moneda especificada. Devuelve None si el modelo no se encuentra
              en la estructura de precios.
    """
def calcular_costo_openai(tokens_entrada, tokens_salida, modelo, precios_modelos, moneda="USD"):

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
    precios = {
        "GPT-4": {"entrada": 0.002, "salida": 0.008},
        "gpt-3.5-turbo": {"entrada": 0.0015, "salida": 0.002}
    }

    texto_entrada = "Escribe un breve poema sobre la primavera."
    texto_salida = "El sol despierta la tierra dormida,\nLas flores brotan en alegre partida.\nEl aire se llena de dulce fragancia,\nY la vida renace con elegancia."

    modelo_gpt4 = "GPT-4"
    tokens_entrada_gpt4 = contar_tokens_openai(texto_entrada, modelo_gpt4)
    tokens_salida_gpt4 = contar_tokens_openai(texto_salida, modelo_gpt4)
    costos_gpt4 = calcular_costo_openai(tokens_entrada_gpt4, tokens_salida_gpt4, modelo_gpt4, precios, "USD")

    print(f"Modelo: {modelo_gpt4}")
    print(f"  Tokens Entrada: {tokens_entrada_gpt4}")
    print(f"  Tokens Salida: {tokens_salida_gpt4}")
    print(f"  Costos (USD): {costos_gpt4}")

    modelo_turbo = "gpt-3.5-turbo"
    tokens_entrada_turbo = contar_tokens_openai(texto_entrada, modelo_turbo)
    tokens_salida_turbo = contar_tokens_openai(texto_salida, modelo_turbo)
    costos_turbo = calcular_costo_openai(tokens_entrada_turbo, tokens_salida_turbo, modelo_turbo, precios, "EUR")

    print(f"\nModelo: {modelo_turbo}")
    print(f"  Tokens Entrada: {tokens_entrada_turbo}")
    print(f"  Tokens Salida: {tokens_salida_turbo}")
    print(f"  Costos (EUR): {costos_turbo}")

    modelo_no_existente = "modelo-inventado"
    tokens_no_existente = contar_tokens_openai(texto_entrada, modelo_no_existente)
    costos_no_existente = calcular_costo_openai(100, 50, modelo_no_existente, precios)

    print(f"\nModelo: {modelo_no_existente}")
    print(f"  Tokens: {tokens_no_existente}")
    print(f"  Costos: {costos_no_existente}")