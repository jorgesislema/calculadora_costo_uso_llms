import tiktoken
"""
Esta función cuenta el número de tokens en un texto dado para un modelo específico.
Los modelos de OpenAI tienen diferentes codificaciones, y esta función utiliza la biblioteca tiktoken para determinar el número de tokens en el texto según el modelo especificado.
Args:
    texto (str): El texto para tokenizar.
    modelo (str): El nombre del modelo de lenguaje (ej. "gpt-4", "cl100k_base").
    Returns:
    int: El número de tokens en el texto para el modelo especificado.
         Devuelve None si no se puede encontrar la codificación para el modelo.
"""
def contar_tokens(texto, modelo):
    try:
        encoding = tiktoken.encoding_for_model(modelo)
        return len(encoding.encode(texto))
    except KeyError:
        try:
            encoding = tiktoken.get_encoding(modelo)
            return len(encoding.encode(texto))
        except KeyError:
            return None

if __name__ == "__main__":
    texto_ejemplo = "Este es un texto de ejemplo para contar tokens."

    modelos_openai = ["gpt-4", "gpt-3.5-turbo", "text-davinci-003", "cl100k_base"]
    for modelo in modelos_openai:
        tokens = contar_tokens(texto_ejemplo, modelo)
        if tokens is not None:
            print(f"Modelo: {modelo}, Tokens: {tokens}")
        else:
            print(f"Modelo: {modelo}, Codificación no encontrada.")

    # Ejemplo con una codificación específica
    codificacion_ejemplo = "r50k_base"
    tokens_especifico = contar_tokens(texto_ejemplo, codificacion_ejemplo)
    if tokens_especifico is not None:
        print(f"\nCodificación: {codificacion_ejemplo}, Tokens: {tokens_especifico}")
    else:
        print(f"\nCodificación: {codificacion_ejemplo}, Codificación no encontrada.")

    texto_largo_ejemplo = "Repite la palabra 'hola' cien veces. " * 100
    modelo_largo = "gpt-3.5-turbo"
    tokens_largo = contar_tokens(texto_largo_ejemplo, modelo_largo)
    if tokens_largo is not None:
        print(f"\nModelo: {modelo_largo}, Tokens en texto largo: {tokens_largo}")
    else:
        print(f"\nModelo: {modelo_largo}, Codificación no encontrada para texto largo.")