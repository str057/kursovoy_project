from unittest.mock import patch
from src.views import main_function


# Тестирование функции main_function
@patch("src.views.get_greeting")
@patch("src.views.get_card_data")
@patch("src.views.get_top_transactions")
@patch("src.views.get_currency_rates")
@patch("src.views.get_stock_prices")
def test_main_function(
    mock_get_stock_prices,
    mock_get_currency_rates,
    mock_get_top_transactions,
    mock_get_card_data,
    mock_get_greeting,
):
    # Настройка моков
    mock_get_greeting.return_value = "Доброе утро"
    mock_get_card_data.return_value = [
        {"last_digits": "5814", "total_spent": 1262.00, "cashback": 12.62},
        {"last_digits": "7512", "total_spent": 7.94, "cashback": 0.08},
    ]
    mock_get_top_transactions.return_value = [
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
    ]
    mock_get_currency_rates.return_value = [
        {"currency": "USD", "rate": 1.0},
        {"currency": "EUR", "rate": 0.85},
    ]
    mock_get_stock_prices.return_value = [
        {"stock": "AAPL", "price": 150.0},
        {"stock": "AMZN", "price": 3200.0},
    ]

    # Вызов функции
    date_time_str = "2023-01-01 09:00:00"
    response = main_function(date_time_str)
    # Проверка результата
    assert response["greeting"] == "Доброе утро"
    assert len(response["cards"]) == 2
    assert response["cards"][0]["last_digits"] == "5814"
    assert len(response["top_transactions"]) == 2
    assert response["currency_rates"][0]["currency"] == "USD"
    assert response["stock_prices"][0]["stock"] == "AAPL"
