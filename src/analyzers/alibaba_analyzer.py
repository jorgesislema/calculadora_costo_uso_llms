"""
Este módulo contendrá funciones específicas para analizar texto con modelos de Alibaba (Qwen).
¡Ojo! La forma exacta de tokenizar y los precios pueden requerir información actualizada
# de la API de Alibaba Cloud Model Studio. Este es un esquema inicial.

Alibaba Qwen utiliza una tokenización BPE y el paquete `qwen-tokenizer` está disponible.
"""

try:
    from qwen_tokenizer import QwenTokenizer
    HAVE_QWEN_TOKENIZER = True
except ImportError:
    HAVE_QWEN_TOKENIZER = False
    print("Advertencia: La librería `qwen-tokenizer` no está instalada. Se usará una estimación basada en palabras.")

def contar_tokens_qwen(texto):
    """
    Estta función cuenta el número de tokens en un texto para modelos Qwen utilizando la librería `qwen-tokenizer`.

    Args:
        texto (str): El texto para tokenizar.

    Returns:
        int: El número de tokens en el texto. Devuelve None si la librería no está instalada.
    """
    if HAVE_QWEN_TOKENIZER:
        tokenizer = QwenTokenizer()
        return len(tokenizer.encode(texto))
    else:
        # Estimación basada en palabras si la librería no está instalada
        return int(len(texto.split()) * 0.8) if texto else 0  # Un factor ligeramente diferente

def calcular_costo_qwen(tokens_entrada, tokens_salida, modelo, precios_modelos, moneda="USD"):
    """
    Esta funcion calcula el costo estimado de tokens de entrada y salida para un modelo de Alibaba Qwen.

    Args:
        tokens_entrada (int): Número de tokens en el prompt de entrada.
        tokens_salida (int): Número de tokens en la salida generada.
        modelo (str): Nombre del modelo Qwen (ej. "Qwen-Max", "Qwen-Turbo").
        precios_modelos (dict): Diccionario con las tarifas por 1000 tokens para cada modelo Qwen.
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
    # Ejemplo de uso
    precios_qwen_ejemplo = {
        "Qwen-Max": {"entrada": 0.0016, "salida": 0.0064},
        "Qwen-Plus": {"entrada": 0.0004, "salida": 0.0012},
        "Qwen-Turbo": {"entrada": 0.00005, "salida": 0.0002},
    }

    texto_entrada_qwen = "¿Cuál es la capital de China?"
    texto_salida_qwen = "La capital de China es Beijing."

    for modelo in ["Qwen-Max", "Qwen-Turbo", "Qwen-Modelo-Inventado"]:
        tokens_entrada = contar_tokens_qwen(texto_entrada_qwen)
        tokens_salida = contar_tokens_qwen(texto_salida_qwen)
        costos = calcular_costo_qwen(tokens_entrada, tokens_salida, modelo, precios_qwen_ejemplo)

        print(f"\nModelo: {modelo}")
        if costos:
            print(f"  Tokens Entrada: {tokens_entrada}")
            print(f"  Tokens Salida: {tokens_salida}")
            print(f"  Costos: {costos}")
        else:
            print("  Costos: No disponible (modelo no encontrado)")

# NOTA: Para una implementación precisa, asegúrate de tener `qwen-tokenizer` instalado.
