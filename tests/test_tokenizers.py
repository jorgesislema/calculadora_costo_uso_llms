import unittest
from src.utils import tokenizers

class TestTokenizers(unittest.TestCase):

    def test_contar_tokens_openai_gpt4(self):
        texto = "Este es un texto de prueba para GPT-4."
        modelo = "gpt-4"
        tokens = tokenizers.contar_tokens(texto, modelo)
        self.assertIsNotNone(tokens)
        self.assertIsInstance(tokens, int)
        self.assertGreater(tokens, 0)

    def test_contar_tokens_openai_gpt35turbo(self):
        texto = "Another test sentence for gpt-3.5-turbo."
        modelo = "gpt-3.5-turbo"
        tokens = tokenizers.contar_tokens(texto, modelo)
        self.assertIsNotNone(tokens)
        self.assertIsInstance(tokens, int)
        self.assertGreater(tokens, 0)

    def test_contar_tokens_openai_modelo_no_existente(self):
        texto = "Texto para un modelo inexistente."
        modelo = "modelo-que-no-existe"
        tokens = tokenizers.contar_tokens(texto, modelo)
        self.assertIsNone(tokens)

    def test_contar_tokens_con_texto_vacio(self):
        texto = ""
        modelo = "gpt-4"
        tokens = tokenizers.contar_tokens(texto, modelo)
        self.assertEqual(tokens, 0)

    def test_contar_tokens_con_caracteres_especiales(self):
        texto = "!@#$%^&*()_+=-`~[]{}\|;':\",./<>?"
        modelo = "gpt-3.5-turbo"
        tokens = tokenizers.contar_tokens(texto, modelo)
        self.assertIsNotNone(tokens)
        self.assertIsInstance(tokens, int)
        self.assertGreater(tokens, 0)

if __name__ == '__main__':
    unittest.main()