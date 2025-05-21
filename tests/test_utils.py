import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime  # Импортируем datetime
from src.utils import (
    get_greeting,
    get_card_data,
    get_top_transactions,
    get_currency_rates,
    get_stock_prices,
)  # Замените your_module на имя вашего файла


class TestFinanceFunctions(unittest.TestCase):
    def test_get_greeting_morning(self):
        time = datetime(2021, 12, 1, 9, 0, 0)  # 9:00 AM
        self.assertEqual(get_greeting(time), "Доброе утро")

    def test_get_greeting_afternoon(self):
        time = datetime(2021, 12, 1, 15, 0, 0)  # 3:00 PM
        self.assertEqual(get_greeting(time), "Добрый день")

    def test_get_greeting_evening(self):
        time = datetime(2021, 12, 1, 19, 0, 0)  # 7:00 PM
        self.assertEqual(get_greeting(time), "Добрый вечер")

    def test_get_greeting_night(self):
        time = datetime(2021, 12, 1, 2, 0, 0)  # 2:00 AM
        self.assertEqual(get_greeting(time), "Доброй ночи")

    def test_get_card_data(self):
        cards = get_card_data()
        self.assertEqual(len(cards), 2)
        self.assertEqual(cards[0]["last_digits"], "5814")
        self.assertEqual(cards[0]["cashback"], 12.62)

    def test_get_top_transactions(self):
        transactions = get_top_transactions()
        self.assertEqual(transactions[0]["amount"], 1198.23)  # Самая большая сумма
        self.assertEqual(transactions[-1]["amount"], -14216.42)  # Самая маленькая сумма

    @patch("requests.get")
    def test_get_currency_rates(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"rates": {"EUR": 0.85, "GBP": 0.75}}
        mock_get.return_value = mock_response
        rates = get_currency_rates()
        self.assertEqual(len(rates), 2)
        self.assertEqual(rates[0]["currency"], "EUR")
        self.assertEqual(rates[0]["rate"], 0.85)

    @patch("requests.get")
    def test_get_stock_prices(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "Meta Data": {"3. Last Refreshed": "2021-12-01"},
            "Time Series (Daily)": {"2021-12-01": {"4. close": "150.00"}},
        }
        mock_get.return_value = mock_response
        prices = get_stock_prices()
        self.assertEqual(prices[0]["stock"], "AAPL")
        self.assertEqual(
            prices[0]["price"], "150.00"
        )  # Убедитесь, что здесь ожидается правильная цена


if __name__ == "__main__":
    unittest.main()
