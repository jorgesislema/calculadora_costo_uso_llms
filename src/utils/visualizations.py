import streamlit as st
import pandas as pd
import plotly.express as px

"""
Este script contiene funciones para mostrar visualizaciones de datos utilizando Streamlit y Plotly.
Las funciones están diseñadas para mostrar comparativas de costos, tokens, energía y emisiones de CO2 entre diferentes modelos de lenguaje.

"""
def mostrar_comparativa_costos(df_resultados, moneda):
    if not df_resultados.empty:
        fig_costos = px.bar(df_resultados, x="Modelo", y=f"Costo Total ({moneda})",
                            title=f"Costo Total Estimado por Modelo ({moneda})")
        st.plotly_chart(fig_costos, use_container_width=True)
    else:
        st.warning("No hay datos de costos para mostrar la comparativa.")
"""
 Esta función muestra un gráfico de barras comparando la cantidad de tokens de entrada y salida por modelo.
"""
def mostrar_comparativa_tokens(df_resultados):
   
    if not df_resultados.empty:
        df_tokens = df_resultados[["Modelo", "Tokens Entrada", "Tokens Salida"]].melt(
            id_vars="Modelo", var_name="Tipo de Token", value_name="Cantidad"
        )
        fig_tokens = px.bar(df_tokens, x="Modelo", y="Cantidad", color="Tipo de Token",
                           title="Cantidad de Tokens de Entrada y Salida por Modelo", barmode="group")
        st.plotly_chart(fig_tokens, use_container_width=True)
    else:
        st.warning("No hay datos de tokens para mostrar la comparativa.")

    """
    Esta función muestra un gráfico de barras comparando el gasto energético estimado por modelo.
    Los datos de energía se obtienen de un DataFrame que contiene la electricidad y el agua consumida por cada modelo.
    """
def mostrar_comparativa_energia(df_resultados):

    if not df_resultados.empty:
        df_energia = df_resultados[["Modelo", "Electricidad (kWh)", "Agua (litros)"]].melt(
            id_vars="Modelo", var_name="Tipo de Gasto", value_name="Cantidad"
        )
        fig_energia = px.bar(df_energia, x="Modelo", y="Cantidad", color="Tipo de Gasto",
                            title="Gasto Energético Estimado por Modelo", barmode="group")
        st.plotly_chart(fig_energia, use_container_width=True)
    else:
        st.warning("No hay datos de gasto energético para mostrar la comparativa.")
    """
    Esta función muestra un gráfico de barras comparando las emisiones de CO2 estimadas por modelo.
    """
def mostrar_comparativa_co2(df_resultados):

    if not df_resultados.empty and "CO2 (kg)" in df_resultados.columns:
        fig_co2 = px.bar(df_resultados, x="Modelo", y="CO2 (kg)",
                            title="Emisiones de CO2 Estimadas por Modelo")
        st.plotly_chart(fig_co2, use_container_width=True)
    else:
        st.warning("No hay datos de emisiones de CO2 para mostrar la comparativa.")

if __name__ == "__main__":
    # Ejemplo de uso (esto no se ejecutará cuando se importe como módulo)
    data_ejemplo = {
        "Modelo": ["Modelo A", "Modelo B", "Modelo C"],
        "Tokens Entrada": [1000, 1500, 800],
        "Tokens Salida": [500, 1000, 1200],
        "Costo Total (USD)": [1.50, 3.00, 2.00],
        "Electricidad (kWh)": [0.1, 0.2, 0.15],
        "Agua (litros)": [0.4, 0.8, 0.6],
        "CO2 (kg)": [0.05, 0.1, 0.07]
    }
    df_ejemplo = pd.DataFrame(data_ejemplo)

    st.title("Ejemplo de Visualizaciones")

    st.subheader("Comparativa de Costos")
    mostrar_comparativa_costos(df_ejemplo, "USD")

    st.subheader("Comparativa de Tokens")
    mostrar_comparativa_tokens(df_ejemplo)

    st.subheader("Comparativa de Energía")
    mostrar_comparativa_energia(df_ejemplo)

    st.subheader("Comparativa de CO2")
    mostrar_comparativa_co2(df_ejemplo)