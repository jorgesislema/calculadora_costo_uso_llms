
#librerias
import streamlit as st
from streamlit.testing.v1 import AppTest
import pandas as pd
import json

# Mock de las funciones de tokenización para pruebas más rápidas y deterministas
def mock_contar_tokens_openai(texto, modelo):
    return len(texto.split())

def mock_contar_tokens_google(texto):
    return int(len(texto.split()) * 0.8)

def mock_contar_tokens_qwen(texto):
    return int(len(texto.split()) * 0.9)

def mock_contar_tokens_anthropic(texto, modelo):
    return len(texto.split())

def mock_contar_tokens_ernie(texto, modelo):
    return len(texto.split())

def mock_contar_tokens_mistral(texto, modelo):
    return len(texto.split())

# Mock de la función de estimación de energía para pruebas deterministas
def mock_estimar_gasto_energetico(modelo, total_tokens):
    if "gpt-4" in modelo.lower():
        return 0.25 * (total_tokens / 1000), 0.9 * (total_tokens / 1000), 0.45 * 0.25 * (total_tokens / 1000)
    elif "llama" in modelo.lower():
        return 0.1 * (total_tokens / 1000), 0.4 * (total_tokens / 1000), 0.45 * 0.1 * (total_tokens / 1000)
    else:
        return 0.05 * (total_tokens / 1000), 0.2 * (total_tokens / 1000), 0.45 * 0.05 * (total_tokens / 1000)

# Cargar precios de modelos desde el archivo JSON (simulando la carga real)
with open("src/config/model_prices.json", "r") as f:
    precios_modelos_data = json.load()
    precios_modelos = precios_modelos_data
    datos_energia = precios_modelos_data.get("energia", {})

# Mock de la lectura del archivo de supuestos de energía
def mock_open(filename, mode):
    if filename == "docs/supuestos_energia.md":
        class MockFile:
            def __enter__(self):
                return self
            def __exit__(self, *args):
                pass
            def read(self):
                return "# Supuestos de Gasto Energético (Mocked)"
        return MockFile()
    else:
        return open(filename, mode)

# Reemplazar las funciones reales con los mocks para las pruebas
st.session_state["contar_tokens_openai"] = mock_contar_tokens_openai
st.session_state["contar_tokens_google"] = mock_contar_tokens_google
st.session_state["contar_tokens_qwen"] = mock_contar_tokens_qwen
st.session_state["contar_tokens_anthropic"] = mock_contar_tokens_anthropic
st.session_state["contar_tokens_ernie"] = mock_contar_tokens_ernie
st.session_state["contar_tokens_mistral"] = mock_contar_tokens_mistral
st.session_state["estimar_gasto_energetico"] = mock_estimar_gasto_energetico
st.session_state["precios_modelos"] = precios_modelos
st.session_state["datos_energia"] = datos_energia
st.session_state["open"] = mock_open

def test_app_initial_state():
    at = AppTest.from_file("src/app.py").run()
    assert not at.selectbox("Seleccione la Moneda").options
    assert not at.multiselect("Seleccione los Modelos de IA para Analizar").options
    assert at.text_area("Ingrese el Prompt de Entrada").value == ""
    assert at.text_area("Ingrese la Salida Generada (Opcional)").value == ""

def test_app_select_models_and_currency():
    at = AppTest.from_file("src/app.py").run()
    at.multiselect("Seleccione los Modelos de IA para Analizar").select(['GPT-4', 'Claude 3 Sonnet']).run()
    at.selectbox("Seleccione la Moneda").select("EUR").run()
    assert len(at.multiselect("Seleccione los Modelos de IA para Analizar").value) == 2
    assert at.selectbox("Seleccione la Moneda").value == "EUR"

def test_app_enter_text_and_analyze():
    at = AppTest.from_file("src/app.py").run()
    at.text_area("Ingrese el Prompt de Entrada").input("Texto de prueba").run()
    at.multiselect("Seleccione los Modelos de IA para Analizar").select(['GPT-4']).run()
    assert at.text_area("Ingrese el Prompt de Entrada").value == "Texto de prueba"
    assert at.subheader(text="Resultados del Análisis:").exists

def test_app_analyze_with_output():
    at = AppTest.from_file("src/app.py").run()
    at.text_area("Ingrese el Prompt de Entrada").input("Texto de entrada").run()
    at.text_area("Ingrese la Salida Generada (Opcional)").input("Texto de salida").run()
    at.multiselect("Seleccione los Modelos de IA para Analizar").select(['GPT-4']).run()
    assert at.subheader(text="Resultados del Análisis:").exists
    assert at.dataframe().data.shape[0] == 1 # Asegurarse de que se muestra una fila en el dataframe

def test_app_documentation_sidebar():
    at = AppTest.from_file("src/app.py").run()
    at.sidebar.selectbox("Seleccione un documento:").select("Supuestos de Gasto Energético").run()
    assert at.sidebar.subheader(text="Supuestos de Gasto Energético").exists
    assert "Supuestos de Gasto Energético (Mocked)" in at.sidebar.markdown().value

    at.sidebar.selectbox("Seleccione un documento:").select("Fuentes de Datos de Precios").run()
    assert at.sidebar.subheader(text="Fuentes de Datos de Precios").exists
    assert "Los precios de los tokens utilizados" in at.sidebar.markdown().value

    at.sidebar.selectbox("Seleccione un documento:").select("Limitaciones de la Estimación").run()
    assert at.sidebar.subheader(text="Limitaciones de la Estimación").exists
    assert "Es importante entender que los cálculos proporcionados" in at.sidebar.markdown().value

def test_app_no_models_selected():
    at = AppTest.from_file("src/app.py").run()
    at.text_area("Ingrese el Prompt de Entrada").input("Texto").run()
    at.run()
    assert at.warning(text="Por favor, selecciona al menos un modelo de IA para analizar.").exists

