import unittest
from unittest.mock import patch, MagicMock
from pokemon_service import PokemonService
from pokemon_name_translator import PokemonNameTranslator
from pokemon_report import PokemonReport
import os


class TestPokemonService(unittest.TestCase):
    @patch("pokemon_service.requests.get")
    def test_get_pokemon_info_success(self, mock_get):
        # Настраиваем поддельный ответ от API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "name": "pikachu",
            "height": 4,
            "weight": 60
        }
        mock_get.return_value = mock_response
        service = PokemonService()
        result = service.get_pokemon_info("pikachu")
        mock_get.assert_called_once_with("https://pokeapi.co/api/v2/pokemon/pikachu")
        self.assertEqual(result["name"], "pikachu")
        self.assertEqual(result["height"], 4)

    @patch("pokemon_service.requests.get")
    def test_get_pokemon_info_fail(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        service = PokemonService()
        result = service.get_pokemon_info("unknown")
        self.assertIsNone(result)


class TestPokemonNameTranslator(unittest.TestCase):
    @patch("pokemon_name_translator.translate.TranslationServiceClient")
    def test_translate_name(self, mock_client_class):
        mock_client = MagicMock()
        mock_client.translate_text.return_value.translations = [
            MagicMock(translated_text="Pikachu (FR)")
        ]
        mock_client_class.return_value = mock_client
        translator = PokemonNameTranslator()
        result = translator.translate("Pikachu", "fr")
        mock_client.translate_text.assert_called_once()
        self.assertEqual(result, "Pikachu (FR)")


class TestPokemonReport(unittest.TestCase):
    @patch("pokemon_report.pdfkit.from_file")
    def test_generate_report_creates_pdf(self, mock_pdfkit):
        report = PokemonReport()
        pokemon_data = {
            "name": "pikachu",
            "height": 4,
            "weight": 60,
            "abilities": [{"ability": {"name": "lightning-rod"}}]
        }
        output_file = "test_pokemon_report.pdf"
        report.generate_report(pokemon_data, "Пикачу", output_file)
        mock_pdfkit.assert_called_once()


class TestIntegration(unittest.TestCase):
    @patch("main.PokemonReport")
    @patch("main.PokemonNameTranslator")
    @patch("main.PokemonService")
    def test_main_flow(self, mock_service_class, mock_translator_class, mock_report_class):
        mock_service = MagicMock()
        mock_service.get_pokemon_info.return_value = {"name": "pikachu"}
        mock_service_class.return_value = mock_service
        mock_translator = MagicMock()
        mock_translator.translate.return_value = "Пикачу"
        mock_translator_class.return_value = mock_translator
        mock_report = MagicMock()
        mock_report_class.return_value = mock_report
        import main
        main.main()
        mock_service.get_pokemon_info.assert_called_once_with("pikachu")
        mock_translator.translate.assert_called_once()
        mock_report.generate_report.assert_called_once()



if __name__ == "__main__":
    unittest.main()
