import json
"""
Esta función calcula el costo estimado de tokens de entrada y salida para un modelo específico.
Los costos se calculan en función de las tarifas por 1000 tokens para cada modelo.
Args:
    tokens_entrada (int): Número de tokens en el prompt de entrada.
    tokens_salida (int): Número de tokens en la salida generada.
    modelo (str): Nombre del modelo de lenguaje.
    precios_modelos (dict): Diccionario con las tarifas por 1000 tokens para cada modelo.
"""
def calcular_costo_tokens(tokens_entrada, tokens_salida, modelo, precios_modelos, moneda="USD"):

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
        "GPT-3.5-turbo": {"entrada": 0.0015, "salida": 0.002}
    }

    resultado_gpt4 = calcular_costo_tokens(1500, 800, "GPT-4", precios, "EUR")
    print(f"Costo para GPT-4: {resultado_gpt4}")

    resultado_turbo = calcular_costo_tokens(2000, 1200, "GPT-3.5-turbo", precios)
    print(f"Costo para GPT-3.5-turbo: {resultado_turbo}")

    resultado_desconocido = calcular_costo_tokens(1000, 500, "Modelo Desconocido", precios)
    print(f"Costo para Modelo Desconocido: {resultado_desconocido}")