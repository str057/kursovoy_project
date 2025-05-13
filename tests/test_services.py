import unittest
from unittest.mock import patch
import pandas as pd
import json


# Импортируем функции, которые мы будем тестировать
from src.services import load_cashback_data_from_excel, analyze_cashback_categories


class TestCashbackAnalysis(unittest.TestCase):
    @patch("pandas.read_excel")
    def test_load_cashback_data_from_excel(self, mock_read_excel):
        # Подготовка тестовых данных
        test_data = pd.DataFrame(
            {
                "date": ["2023-10-01", "2023-10-02"],
                "category": ["Food", "Transport"],
                "cashback": [100, 50],
            }
        )
        mock_read_excel.return_value = test_data
        # Вызов функции
        result = load_cashback_data_from_excel("dummy_path.xlsx")
        # Проверка результата
        expected_result = [
            {"date": "2023-10-01", "category": "Food", "cashback": 100},
            {"date": "2023-10-02", "category": "Transport", "cashback": 50},
        ]
        self.assertEqual(result, expected_result)

    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    @patch("json.dumps")
    def test_analyze_cashback_categories(self, mock_json_dumps, mock_open):
        # Подготовка тестовых данных
        test_data = [
            {"date": "2023-10-01", "category": "Food", "cashback": 100},
            {"date": "2023-10-02", "category": "Transport", "cashback": 50},
            {"date": "2023-10-01", "category": "Food", "cashback": 150},
        ]
        mock_json_dumps.return_value = json.dumps({"Food": 250, "Transport": 50})
        # Вызов функции
        analyze_cashback_categories(test_data, 2023, 10, "dummy_output.json")
        # Проверка, что json.dumps был вызван с правильными данными
        mock_json_dumps.assert_called_once_with(
            {"Food": 250, "Transport": 50}, ensure_ascii=False
        )
        # Проверка, что файл был открыт для записи
        mock_open.assert_called_once_with("dummy_output.json", "w", encoding="utf-8")
        # Проверка, что данные были записаны в файл
        mock_open().write.assert_called_once_with(mock_json_dumps.return_value)


if __name__ == "__main__":
    unittest.main()
