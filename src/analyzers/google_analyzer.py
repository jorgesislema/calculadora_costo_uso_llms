"""
Este módulo para calcular costos de uso de modelos de Google AI (Gemini) y estimar tokens.
Este módulo incluye funciones para contar tokens y calcular costos estimados de entrada y salida
¡Ojo! La forma exacta de tokenizar y los precios pueden requerir información actualizada
#de la API de Google AI y Vertex AI. Este es un esquema inicial.

Por el momento, no hay una librería de tokenización específica de Google AI fácil de usar
como `tiktoken` para OpenAI. La API de Gemini tiene métodos para contar tokens,
pero para una implementación local, podríamos usar una aproximación basada en palabras
o investigar librerías como SentencePiece que Google utiliza internamente.
"""
#libreria
import tiktoken
"""
Esta función estima el número de tokens en un texto para modelos de Google (aproximación basada en palabras).
"""
def contar_tokens_google(texto):

    # Una aproximación simple es dividir el número de palabras por un factor (ej: 0.75).
    # Esto se basa en la heurística de que en promedio, un token es ~0.75 palabras en inglés.
    # Para otros idiomas, este factor podría variar.
    return int(len(texto.split()) * 0.75) if texto else 0
"""
Esta funcion estima el costo de tokens de entrada y salida para un modelo de Google.
Los costos se calculan en función de las tarifas por 1000 tokens para cada modelo.

"""
def calcular_costo_google(tokens_entrada, tokens_salida, modelo, precios_modelos, moneda="USD"):
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
    precios_google_ejemplo = {
        "Gemini 2.5 Pro Preview": {"entrada": 0.00125, "salida": 0.01},
        "Gemini 1.5 Flash": {"entrada": 0.000075, "salida": 0.0003},
        "Gemini 2.0 Flash-Lite": {"entrada": 0.000075, "salida": 0.0003},
    }

    texto_entrada_google = "Explica la teoría de la relatividad en dos frases."
    texto_salida_google = "La teoría de la relatividad especial describe cómo el espacio y el tiempo están entrelazados para objetos que se mueven a velocidades constantes. La teoría de la relatividad general explica cómo la gravedad es la curvatura del espacio-tiempo causada por la masa y la energía."

    modelo_gemini_pro = "Gemini 2.5 Pro Preview"
    tokens_entrada_google_pro = contar_tokens_google(texto_entrada_google)
    tokens_salida_google_pro = contar_tokens_google(texto_salida_google)
    costos_google_pro = calcular_costo_google(tokens_entrada_google_pro, tokens_salida_google_pro, modelo_gemini_pro, precios_google_ejemplo, "USD")

    print(f"Modelo: {modelo_gemini_pro}")
    print(f"  Tokens Entrada (estimado): {tokens_entrada_google_pro}")
    print(f"  Tokens Salida (estimado): {tokens_salida_google_pro}")
    print(f"  Costos (USD): {costos_google_pro}")

    modelo_gemini_flash = "Gemini 1.5 Flash"
    tokens_entrada_google_flash = contar_tokens_google(texto_entrada_google)
    tokens_salida_google_flash = contar_tokens_google(texto_salida_google)
    costos_google_flash = calcular_costo_google(tokens_entrada_google_flash, tokens_salida_google_flash, modelo_gemini_flash, precios_google_ejemplo, "EUR")

    print(f"\nModelo: {modelo_gemini_flash}")
    print(f"  Tokens Entrada (estimado): {tokens_entrada_google_flash}")
    print(f"  Tokens Salida (estimado): {tokens_salida_google_flash}")
    print(f"  Costos (EUR): {costos_google_flash}")

    modelo_no_existente_google = "Modelo Gemini Desconocido"
    costos_no_existente_google = calcular_costo_google(100, 50, modelo_no_existente_google, precios_google_ejemplo)
    print(f"\nModelo: {modelo_no_existente_google}, Costos: {costos_no_existente_google}")
"""
NOTA IMPORTANTE: Para una implementación precisa con modelos de Google,
se recomienda utilizar la API de Gemini y su funcionalidad para contar tokens.
Las aproximaciones locales pueden no ser exactas.
"""