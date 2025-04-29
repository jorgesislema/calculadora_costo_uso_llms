import json
"""
Esta funcion nos ayuda a calcular cuánta energía y agua se gasta al usar cada modelo.
Los datos de energía y agua se obtienen de un archivo JSON que contiene los supuestos de consumo energético por modelo.
Los datos de energía y agua se pueden modificar en el archivo JSON para ajustar los cálculos según sea necesario.

"""
def estimar_gasto_energetico(modelo, total_tokens, datos_energia):

    modelo_lower = modelo.lower()
    electricidad_por_1k = None
    agua_por_1k = None

    for key, valores in datos_energia.items():
        if key.lower() in modelo_lower:
            electricidad_por_1k = valores.get("electricidad_por_1k_tokens")
            agua_por_1k = valores.get("agua_por_1k_tokens")
            break

    if electricidad_por_1k is not None and agua_por_1k is not None:
        gasto_electricidad = (total_tokens / 1000) * electricidad_por_1k
        gasto_agua = (total_tokens / 1000) * agua_por_1k
        return gasto_electricidad, gasto_agua
    else:
        # Supuestos para modelos no especificados individualmente
        if "gpt-4" in modelo_lower or "claude 3 opus" in modelo_lower or "gemini 2.5 pro" in modelo_lower:
            return (total_tokens / 1000) * 0.25, (total_tokens / 1000) * 0.9
        elif "gemini pro" in modelo_lower or "claude 3 sonnet" in modelo_lower() or "llama 3.3 70b" in modelo_lower():
            return (total_tokens / 1000) * 0.1, (total_tokens / 1000) * 0.4
        elif "mistral large" in modelo_lower or "qwen-max" in modelo_lower or "glm-4-plus" in modelo_lower():
            return (total_tokens / 1000) * 0.15, (total_tokens / 1000) * 0.6
        else: # Modelos más pequeños o desconocidos
            return (total_tokens / 1000) * 0.04, (total_tokens / 1000) * 0.15

if __name__ == "__main__":
    # Ejemplo de uso (esto no se ejecutará cuando se importe como módulo)
    datos_energia_ejemplo = {
        "gpt-4": {"electricidad_por_1k_tokens": 0.25, "agua_por_1k_tokens": 0.9},
        "llama 3.70b": {"electricidad_por_1k_tokens": 0.1, "agua_por_1k_tokens": 0.4},
        "mistral large": {"electricidad_por_1k_tokens": 0.15, "agua_por_1k_tokens": 0.6}
    }

    modelo_ejemplo_1 = "GPT-4"
    tokens_ejemplo_1 = 2500
    electricidad_1, agua_1 = estimar_gasto_energetico(modelo_ejemplo_1, tokens_ejemplo_1, datos_energia_ejemplo)
    print(f"Estimación para {modelo_ejemplo_1} ({tokens_ejemplo_1} tokens):")
    print(f"  Electricidad: {electricidad_1:.4f} kWh")
    print(f"  Agua: {agua_1:.4f} litros")

    modelo_ejemplo_2 = "Llama 3.70B"
    tokens_ejemplo_2 = 5000
    electricidad_2, agua_2 = estimar_gasto_energetico(modelo_ejemplo_2, tokens_ejemplo_2, datos_energia_ejemplo)
    print(f"\nEstimación para {modelo_ejemplo_2} ({tokens_ejemplo_2} tokens):")
    print(f"  Electricidad: {electricidad_2:.4f} kWh")
    print(f"  Agua: {agua_2:.4f} litros")

    modelo_ejemplo_3 = "Modelo Desconocido"
    tokens_ejemplo_3 = 1000
    electricidad_3, agua_3 = estimar_gasto_energetico(modelo_ejemplo_3, tokens_ejemplo_3, datos_energia_ejemplo)
    print(f"\nEstimación para {modelo_ejemplo_3} ({tokens_ejemplo_3} tokens):")
    print(f"  Electricidad: {electricidad_3:.4f} kWh")
    print(f"  Agua: {agua_3:.4f} litros")