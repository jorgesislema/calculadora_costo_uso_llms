# Calculadora de Costo y Tokens de Modelos de IA

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://token-analyzer.streamlit.app/)

Esta aplicación web interactiva, desarrollada con Streamlit, permite analizar el costo, el consumo de tokens (entrada/salida) y una estimación del gasto energético y huella de carbono (CO2) asociados al uso de modelos de lenguaje (LLMs) como GPT, Claude, Gemini, Mistral, entre otros.

---

## 🚀 Características Principales

- **📈 Análisis de Tokenización:** Calcula tokens de entrada/salida usando `tiktoken` para modelos OpenAI y estimaciones para otros.
- **💰 Cálculo de Costos:** Estima costos de tokens de entrada, salida y total según tarifas actualizadas por modelo.
- **⚡ Estimación Energética:** Calcula consumo aproximado de electricidad (kWh) y agua (litros) por tokens procesados.
- **🌍 Emisiones de CO2:** Estima la huella de carbono (kg CO2) basándose en consumo eléctrico y un factor global.
- **🔧 Interfaz Intuitiva:** Entradas de texto fáciles de usar y selección múltiple de modelos y moneda.
- **📊 Visualizaciones Interactivas:** Gráficos de barras comparativos de costos y gasto ambiental con Plotly.
- **🔍 Documentación Integrada:** Acceso contextual a supuestos, fuentes y limitaciones desde la barra lateral.

---

## 🔄 Cómo Utilizar

1. **Ingresa el Prompt de Entrada:** Escribe o pega tu texto en el área "Prompt de entrada".
2. **(Opcional) Ingresa la Salida:** Si tienes la respuesta generada, pégala para calcular tokens y costos de salida.
3. **Selecciona los Modelos:** Usa el selector para elegir uno o varios LLMs a analizar.
4. **Elige la Moneda:** Cambia entre USD y EUR según tu preferencia.
5. **Analiza los Resultados:** Revisa la tabla con tokens, costos y estimaciones ambientales.
6. **Explora los Gráficos:** Compara visualmente los resultados entre modelos.
7. **Lee la Documentación:** Usa el panel lateral para comprender los criterios técnicos.

---

## 🛠 Instalación Local

```bash
# Clona este repositorio
git clone https://github.com/jorgesislema/calculadora-costo-uso-llms.git
cd calculadora-costo-uso-llms

# (Opcional) Crea un entorno virtual
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Instala dependencias
pip install -r requirements.txt

# Ejecuta la app
streamlit run src/app.py
```

---

## 📁 Estructura del Proyecto

```text
calculadora-costo-uso-llms/
├── docs/
│   ├── supuestos_energia.md
│   ├── fuentes_precios.md
│   └── limitaciones.md
├── src/
│   ├── app.py
│   ├── analyzers/
│   ├── calculators/
│   ├── config/
│   └── utils/
├── tests/
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 📦 Dependencias

```bash
pip install -r requirements.txt
```

- `streamlit` — interfaz interactiva
- `pandas` — manipulación de datos
- `plotly-express` — visualizaciones interactivas
- `tiktoken` — tokenización precisa para modelos OpenAI

---

## 🔗 Enlace a la Aplicación

👉 [https://token-analyzer.streamlit.app](https://token-analyzer.streamlit.app)

---

## ℹ️ Notas Importantes

- Las estimaciones de energía y CO2 se basan en supuestos generales y pueden variar según infraestructura y ubicación.
- La tokenización para modelos no-OpenAI se aproxima dividiendo palabras por 4 (puede no ser precisa).
- Las tarifas de tokens están basadas en fuentes oficiales públicas y pueden cambiar con el tiempo.

---

## 📝 Contribuciones

Contribuciones, mejoras y nuevas funcionalidades son bienvenidas. 
Puedes abrir issues o enviar un Pull Request ¡Gracias!

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
