calculadora-costo-uso-llms/
├── .github/
│   └── workflows/
│       └── main.yml            # (CI/CD opcional)
│
├── docs/
│   ├── supuestos_energia.md     # Metodología de estimaciones ambientales
│   ├── fuentes_precios.md       # De dónde se obtuvieron precios de tokens
│   └── limitaciones.md          # Declaraciones de limitaciones y supuestos
│
├── src/
│   ├── app.py                   # Código principal de la aplicación Streamlit
│   ├── config/
│   │   └── model_prices.json     # Precios de tokens y parámetros ambientales
│   ├── analyzers/
│   │   ├── openai_analyzer.py    # Tokenizer y costos OpenAI
│   │   ├── google_analyzer.py    # Tokenizer y costos Google Gemini
│   │   ├── mistral_analyzer.py   # Tokenizer y costos Mistral
│   │   └── ...                   # Otros proveedores
│   ├── calculators/
│   │   ├── token_costs.py        # Cálculo de costos de entrada y salida
│   │   └── energy_estimation.py  # Estimación de gasto de energía y agua
│   ├── utils/
│   │   ├── tokenizers.py         # Funciones generales de tokenización
│   │   └── visualizations.py     # Gráficos dinámicos (Plotly, etc.)
│
├── static/
│   ├── images/                   # Capturas de pantalla o gráficos
│   └── videos/                   # Demostraciones opcionales para LinkedIn
│
├── tests/
│   ├── test_tokenizers.py         # Pruebas unitarias de tokenización
│   ├── test_calculators.py        # Pruebas unitarias de costos
│   └── test_app.py                # Pruebas generales de la app
│
├── README.md                      # Descripción general del proyecto
├── requirements.txt               # Dependencias
├── .gitignore                     # Archivos a ignorar por Git
└── LICENSE                        # Licencia de uso (MIT, Apache, etc.)
