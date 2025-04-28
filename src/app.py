"""
Para este proyecto se utilizaremos streamlib, par los calculos de tokens tomamos de base la libreria tiktoken, para los demas modelos los dividiremos en 4 partes:
Ademas calcularemos el gasto energetico y de agua, y el CO2 estimado en base a la energia utilizada.
- Contar tokens de entrada y salida para cada modelo de IA.
- Calcular el costo de los tokens de entrada y salida para cada modelo.
- Calcular el gasto de energía y agua para cada modelo.
- Calcular el CO2 estimado para cada modelo.
- Mostrar los resultados en una tabla y un gráfico de barras.
- Permitir al usuario seleccionar los modelos de IA que desea analizar.
- Permitir al usuario seleccionar la moneda en la que se mostrar

"""
#Librerias
import streamlit as st
import pandas as pd
import tiktoken 
import plotly.express as px

#realizamos un dicionario con los valores de los precios de los diferentes modelos de IA del mercado

precios_modelos = {
    "GPT-4": {"entrada": 0.002, "salida": 0.008},
    "GPT-4o": {"entrada": 0.005, "salida": 0.02},
    "GPT-4o-mini": {"entrada": 0.0011, "salida": 0.0044},
    "Claude 3 Opus": {"entrada": 0.015, "salida": 0.075},
    "Claude 3 Sonnet": {"entrada": 0.003, "salida": 0.015},
    "Claude 3 Haiku": {"entrada": 0.00025, "salida": 0.00125},
    "Gemini 2.5 Pro Preview": {"entrada": 0.00125, "salida": 0.01},
    "Gemini 1.5 Flash": {"entrada": 0.000075, "salida": 0.0003},
    "Gemini 2.0 Flash-Lite": {"entrada": 0.000075, "salida": 0.0003},
    "Llama 3.1 405B": {"entrada": 0.0035, "salida": 0.0035},
    "Llama 3.3 70B": {"entrada": 0.00059, "salida": 0.00099},
    "Llama 3.1 8B": {"entrada": 0.00009, "salida": 0.00009},
    "Mistral Large": {"entrada": 0.003, "salida": 0.009},
    "Codestral": {"entrada": 0.001, "salida": 0.003},
    "Nemo": {"entrada": 0.0003, "salida": 0.0003},
    "ERNIE 4.5": {"entrada": 0.00055, "salida": 0.0022},
    "ERNIE X1": {"entrada": 0.00028, "salida": 0.0011},
    "Qwen-Max": {"entrada": 0.0016, "salida": 0.0064},
    "Qwen-Plus": {"entrada": 0.0004, "salida": 0.0012},
    "Qwen-Turbo": {"entrada": 0.00005, "salida": 0.0002},
    "GLM-4-Plus": {"entrada": 0.0007, "salida": 0.0007},
    "GLM-4-Long": {"entrada": 0.00014, "salida": 0.00014},
    "GLM-4-AirX": {"entrada": 0.0014, "salida": 0.0014},
}

# Suponemos una intensidad de carbono promedio global (kg CO2/kWh).
# Este valor es un ejemplo y puede variar significativamente.
INTENSIDAD_CARBONO_PROMEDIO = 0.45 # kg CO2/kWh (aproximadamente el promedio mundial en 2021)

# Esta función nos ayuda a calcular cuánta energía y agua se gasta al usar cada modelo.
def estimar_gasto_energetico(modelo, total_tokens):
    # Supuestos aproximados (kWh electricidad / 1000 tokens, litros agua / 1000 tokens)
    if "gpt-4" in modelo.lower() or "claude 3 opus" in modelo.lower() or "gemini 2.5 pro" in modelo.lower():
        electricidad = (total_tokens / 1000) * 0.25
        agua = (total_tokens / 1000) * 0.9
    elif "gemini pro" in modelo.lower() or "claude 3 sonnet" in modelo.lower() or "llama 3.3 70b" in modelo.lower():
        electricidad = (total_tokens / 1000) * 0.1
        agua = (total_tokens / 1000) * 0.4
    elif "mistral large" in modelo.lower() or "qwen-max" in modelo.lower() or "glm-4-plus" in modelo.lower():
        electricidad = (total_tokens / 1000) * 0.15
        agua = (total_tokens / 1000) * 0.6
    else: # Modelos más pequeños o desconocidos
        electricidad = (total_tokens / 1000) * 0.04
        agua = (total_tokens / 1000) * 0.15

    co2_estimado = electricidad * INTENSIDAD_CARBONO_PROMEDIO
    return electricidad, agua, co2_estimado

# Tittulo de la aplicacion en streamlit

st.title("Calculadora de Costos y Tokens de Modelos de IA")
st.markdown("Analiza el costo de los ttokens , elgasto energetico y de CO2 esttimado de los modelos de IA.")

#------------------------------------------------------------------------------------------------------------------------------------

#Area donde el usuario puede ingresar el prompt

prompt_entrada= st.text_area("Ingresa tu prompt de entrada:", height=200)

#Area donde el usuario puede ingresar el prompt de salida
prompt_salida = st.text_area("Ingresa tu prompt de salida:(opcional )", height=200)

#------------------------------------------------------------------------------------------------------------------------------------

# Lista de todos los modelos de IA que podemos analizar. ¡Nuestras opciones!
modelos_ia = [
    'GPT-4', 'GPT-4o', 'GPT-4o-mini', 'Claude 3 Opus', 'Claude 3 Sonnet', 'Claude 3 Haiku',
    'Gemini 2.5 Pro Preview', 'Gemini 1.5 Flash', 'Gemini 2.0 Flash-Lite',
    'Llama 3.1 405B', 'Llama 3.3 70B', 'Llama 3.1 8B',
    'Mistral Large', 'Codestral', 'Nemo', 'ERNIE 4.5', 'ERNIE X1',
    'Qwen-Max', 'Qwen-Plus', 'Qwen-Turbo', 'GLM-4-Plus', 'GLM-4-Long', 'GLM-4-AirX'
]

#widget para seleccionar el modelo de IA

modelos_seleccionados = st.multiselect("Selecciona los modelos de IA que deseas analizar:", modelos_ia, default=["GPT-4"])

#Widget para seleccionar la moneda ,('USD', 'EUR')

moneda_seleccionada = st.selectbox("Selecciona la moneda:", ['USD', 'EUR'])

#------------------------------------------------------------------------------------------------------------------------------------
#realizamos los calculos  cuando el usuario a seleccionado los modelos de IA

if modelos_seleccionados:
    st.subheader("Resultados del Análisis")
    resultados = []
    for modelo in modelos_seleccionados:
        tokens_entrada=0
        tokens_salida =0
        costo_entrada = 0
        costo_salida = 0
        costo_total = 0
        gastto_electricidad = 0
        gasto_agua = 0
        gasto_CO2 = 0
        # Contamos los tokens de entrada y salida segun el modelo seleccionado
        if "gpt-4" in modelo.lower() :
            tokens_entrada = contar_tokens_openai(prompt_entrada,modelo)
        else:
            tokens_entrada = len(salida_generada.split()) /4 if salida_generada else 0

#Calculamos los costos de entrada y salida segun el modelo seleccionado
    if modelo in precios_modelos:
        tarifa_entrada = precios_modelos[modelo].get("entrada", 0)
        tarifa_salida = precios_modelos[modelo].get("salida", 0)

        costo_entrada =(tokens_entrada / 1000) * tarifa_entrada
        costo_salida = (tokens_salida / 1000) * tarifa_salida
        costo_total = costo_entrada + costo_salida
        
        total_tokens = tokens_entrada + tokens_salida
        gasto_electricidad, gasto_agua, gasto_CO2 = estimar_gasto_energetico(modelo, total_tokens)

        #Guardamos los resulttados que los mostraremos en la tabla y el grafico
        resultados.append({
            "modelo": modelo,
            "tokens_entrada": tokens_entrada if tokens_entrada is not None else "No disponible",
            f"Costo entrada ({moneda_seleccionada})": f"{costo_entrada:.6f}",
            f"Costo salida ({moneda_seleccionada})": f"{costo_salida:.6f}",
            f"Costo total ({moneda_seleccionada})": f"{costo_total:.6f}",
            "Electricidad (kWh)": f"{gasto_electricidad:.4f}",
            "Agua (litros)": f"{gasto_agua:.4f}",
            "CO2 (kg)": f"{gasto_CO2:.4f}",
        })

        #Mostramos los resultados en una tabla

        



