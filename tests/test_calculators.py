import unittest
from src.calculators import token_costs
from src.calculators import energy_estimation
import json

# Cargar datos de precios y energía para las pruebas
with open("src/config/model_prices.json", "r") as f:
    precios_energia_data = json.load()
    precios_modelos = precios_energia_data
    datos_energia = precios_energia_data.get("energia", {})

class TestTokenCosts(unittest.TestCase):

    def test_calcular_costo_tokens_modelo_existente(self):
        resultado = token_costs.calcular_costo_tokens(1000, 500, "GPT-4", precios_modelos, "USD")
        self.assertEqual(resultado["costo_entrada_USD"], "0.002000")
        self.assertEqual(resultado["costo_salida_USD"], "0.004000")
        self.assertEqual(resultado["costo_total_USD"], "0.006000")

    def test_calcular_costo_tokens_modelo_no_existente(self):
        resultado = token_costs.calcular_costo_tokens(1000, 500, "Modelo Inexistente", precios_modelos, "EUR")
        self.assertIsNone(resultado)

    def test_calcular_costo_tokens_con_moneda_eur(self):
        resultado = token_costs.calcular_costo_tokens(2000, 1000, "Claude 3 Sonnet", precios_modelos, "EUR")
        self.assertEqual(resultado["costo_entrada_EUR"], "0.006000")
        self.assertEqual(resultado["costo_salida_EUR"], "0.015000")
        self.assertEqual(resultado["costo_total_EUR"], "0.021000")

    def test_calcular_costo_tokens_con_tarifas_cero(self):
        precios_prueba = {"Modelo Cero": {"entrada": 0.0, "salida": 0.0}}
        resultado = token_costs.calcular_costo_tokens(500, 200, "Modelo Cero", precios_prueba, "USD")
        self.assertEqual(resultado["costo_entrada_USD"], "0.000000")
        self.assertEqual(resultado["costo_salida_USD"], "0.000000")
        self.assertEqual(resultado["costo_total_USD"], "0.000000")

class TestEnergyEstimation(unittest.TestCase):

    def test_estimar_gasto_energetico_modelo_grande(self):
        electricidad, agua = energy_estimation.estimar_gasto_energetico("GPT-4", 1000, datos_energia)
        self.assertAlmostEqual(electricidad, 0.25)
        self.assertAlmostEqual(agua, 0.9)

    def test_estimar_gasto_energetico_modelo_mediano(self):
        electricidad, agua = energy_estimation.estimar_gasto_energetico("Llama 3.70B", 1000, datos_energia)
        self.assertAlmostEqual(electricidad, 0.1)
        self.assertAlmostEqual(agua, 0.4)

    def test_estimar_gasto_energetico_modelo_pequeno(self):
        electricidad, agua = energy_estimation.estimar_gasto_energetico("Qwen-Turbo", 1000, datos_energia)
        self.assertAlmostEqual(electricidad, 0.04)
        self.assertAlmostEqual(agua, 0.15)

    def test_estimar_gasto_energetico_modelo_especifico(self):
        electricidad, agua = energy_estimation.estimar_gasto_energetico("gpt-4", 2000, datos_energia)
        self.assertAlmostEqual(electricidad, 0.5)
        self.assertAlmostEqual(agua, 1.8)

    def test_estimar_gasto_energetico_modelo_no_especificado(self):
        electricidad, agua = energy_estimation.estimar_gasto_energetico("Modelo Desconocido", 1000, datos_energia)
        self.assertAlmostEqual(electricidad, 0.04)
        self.assertAlmostEqual(agua, 0.15)

if __name__ == '__main__':
    unittest.main()