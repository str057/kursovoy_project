import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from src.utils import (
    get_greeting,
    get_card_data,
    get_top_transactions,
    get_currency_rates,
    get_stock_prices,
)


# Фикстура для генерации тестовых данных
@pytest.fixture
def mock_card_data():
    return [
        {"last_digits": "5814", "total_spent": 1262.00},
        {"last_digits": "7512", "total_spent": 7.94},
    ]


@pytest.fixture
def mock_transactions():
    return [
        {
            "date": "21.12.2021",
            "amount": 1198.23,
            "category": "Переводы",
            "description": "Перевод Кредитная карта. ТП 10.2 RUR",
        },
        {
            "date": "20.12.2021",
            "amount": 829.00,
            "category": "Супермаркеты",
            "description": "Лента",
        },
        {
            "date": "20.12.2021",
            "amount": 421.00,
            "category": "Различные товары",
            "description": "Ozon.ru",
        },
        {
            "date": "16.12.2021",
            "amount": -14216.42,
            "category": "ЖКХ",
            "description": "ЖКУ Квартира",
        },
        {
            "date": "16.12.2021",
            "amount": 453.00,
            "category": "Бонусы",
            "description": "Кешбэк за обычные покупки",
        },
    ]


# Тестирование функции get_greeting
def test_get_greeting():
    assert get_greeting(datetime(2023, 1, 1, 5, 0)) == "Доброй ночи"
    assert get_greeting(datetime(2023, 1, 1, 9, 0)) == "Доброе утро"
    assert get_greeting(datetime(2023, 1, 1, 15, 0)) == "Добрый день"
    assert get_greeting(datetime(2023, 1, 1, 19, 0)) == "Добрый вечер"


# Тестирование функции get_card_data
def test_get_card_data(mock_card_data):
    cards = get_card_data()
    assert len(cards) == len(mock_card_data)
    for card in cards:
        assert "cashback" in card
        assert isinstance(card["cashback"], float)


# Тестирование функции get_top_transactions
def test_get_top_transactions():
    transactions = get_top_transactions()
    assert len(transactions) == 5
    amounts = [t["amount"] for t in transactions]
    assert amounts == sorted(amounts, reverse=True)


# Тестирование функции get_currency_rates с использованием mock
@patch("src.utils.requests.get")
def test_get_currency_rates(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"rates": {"USD": 1.0, "EUR": 0.85}}
    mock_get.return_value = mock_response
    rates = get_currency_rates()
    assert isinstance(rates, list)
    assert any(rate["currency"] == "USD" for rate in rates)
    assert any(
        isinstance(rate["rate"], float) or isinstance(rate["rate"], int)
        for rate in rates
    )


# Тестирование функции get_stock_prices с использованием mock
@patch("src.utils.requests.get")
def test_get_stock_prices(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"price": 150.0}
    mock_get.return_value = mock_response
    stock_prices = get_stock_prices()
    assert isinstance(stock_prices, list)
    assert len(stock_prices) == 5
    for stock in stock_prices:
        assert "stock" in stock
        assert "price" in stock
        assert stock["price"] == 150.0
