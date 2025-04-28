# Supuestos de Gasto Energético para el Cálculo de Costos de LLMs

Este documento detalla los supuestos utilizados para estimar el gasto energético (electricidad y agua) asociado al uso de diferentes modelos de lenguaje de inteligencia artificial (LLMs) en esta calculadora. Es importante tener en cuenta que estos son **estimaciones aproximadas** y pueden variar significativamente en función de la infraestructura subyacente, la eficiencia del hardware, las prácticas de enfriamiento y otros factores.

**Metodología General:**

La estimación se basa en la categorización de los modelos en tres grupos generales (grande, mediano, pequeño/eficiente) y la asignación de un consumo energético promedio por cada 1000 tokens procesados. Estos valores se multiplican por el número total de tokens (entrada + salida) para obtener una estimación del gasto total.

**Categorías de Modelos y Supuestos:**

| Categoría          | Modelos Ejemplo                                                                                                                                                                                             | Electricidad (kWh / 1000 tokens) | Agua (litros / 1000 tokens) | Justificación Aparente                                                                                                                                                                                                                                                           |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------- | ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Grande** | GPT-4, GPT-4o, Claude 3 Opus, Gemini 2.5 Pro Preview                                                                                                                                                         | 0.25                              | 0.9                         | Se asume una mayor complejidad y tamaño del modelo, lo que implica una mayor demanda computacional y, por ende, un mayor consumo energético para el entrenamiento e inferencia. Los procesos de enfriamiento para la infraestructura que soporta estos modelos también se estima que son más intensivos en el uso de agua.                                                              |
| **Mediano** | Claude 3 Sonnet, Llama 3.70B, Mistral Large, Qwen-Max, GLM-4-Plus                                                                                                                                          | 0.1                               | 0.4                         | Estos modelos representan un punto intermedio en tamaño y complejidad, con un consumo energético y necesidades de enfriamiento moderados en comparación con los modelos más grandes.                                                                                                                                                                                                     |
| **Pequeño/Eficiente** | GPT-4o-mini, Claude 3 Haiku, Gemini 1.5 Flash, Gemini 2.0 Flash-Lite, Llama 3.1 8B, Codestral, Nemo, ERNIE 4.5, ERNIE X1, Qwen-Plus, Qwen-Turbo, GLM-4-Long, GLM-4-AirX                                         | 0.04                              | 0.15                        | Se asume que estos modelos están optimizados para la eficiencia, con un menor tamaño y menor demanda computacional, lo que resulta en un menor consumo de electricidad y una menor necesidad de enfriamiento intensivo en agua.                                                                                                                                              |

**Advertencia Importante:**

Los valores presentados en esta tabla son **estimaciones basadas en suposiciones generales**. El gasto energético real puede variar considerablemente debido a:

* **Infraestructura específica:** La eficiencia del hardware (GPUs, TPUs), el diseño de los centros de datos y las tecnologías de enfriamiento utilizadas pueden tener un impacto significativo.
* **Utilización de recursos:** La carga del servidor y la eficiencia del software de inferencia influyen en el consumo energético por token.
* **Ubicación geográfica:** El mix energético de la región donde se aloja la infraestructura afecta la huella de carbono asociada al consumo de electricidad.
* **Procesos de entrenamiento vs. inferencia:** Los costos energéticos del entrenamiento de los modelos son significativamente mayores que los de la inferencia, y esta calculadora se centra en el uso (inferencia).
* **Evolución tecnológica:** La eficiencia de los modelos y el hardware está en constante mejora.

**Uso de los Datos:**

Estas estimaciones proporcionan una **orden de magnitud aproximado** del posible gasto energético relativo entre diferentes categorías de modelos. No deben interpretarse como valores precisos o definitivos.

