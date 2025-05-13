import json
import os
import logging
import requests
from datetime import datetime
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()
# Получение ключа API из переменных окружения
API_KEY = os.getenv("API_KEY")
if API_KEY is None:
    raise ValueError("API_KEY не установлен в .env файле")
logging.basicConfig(level=logging.INFO)


def load_currency_rates_from_file():
    with open("glavnaya.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        return data.get("rates", {})


def get_greeting(current_time):
    if current_time.hour < 6:
        return "Доброй ночи"
    elif current_time.hour < 12:
        return "Доброе утро"
    elif current_time.hour < 18:
        return "Добрый день"
    else:
        return "Добрый вечер"


def get_card_data():
    # Пример данных о картах
    cards = [
        {"last_digits": "5814", "total_spent": 1262.00},
        {"last_digits": "7512", "total_spent": 7.94},
    ]
    for card in cards:
        card["cashback"] = round(card["total_spent"] / 100, 2)
    return cards


def get_top_transactions():
    # Пример данных о транзакциях
    transactions = [
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
    # Отделяем функцию get_top_transactions от следующей функции пустой строкой
    return sorted(transactions, key=lambda x: x["amount"], reverse=True)


def get_currency_rates():
    # Пример запроса к API для получения курсов валют
    response = requests.get(
        f"https://api.exchangerate-api.com/v4/latest/USD?apikey={API_KEY}"
    )
    rates = response.json().get("rates", {})
    return [{"currency": currency, "rate": rate} for currency, rate in rates.items()]


def get_stock_prices():
    # Пример запроса к API для получения цен акций
    stocks = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    prices = {}
    for stock in stocks:
        response = requests.get(
            f"https://api.example.com/stocks/{stock}?apikey={API_KEY}"
        )
        prices[stock] = response.json().get("price", 0)
    return [{"stock": stock, "price": prices[stock]} for stock in stocks]


current_time = datetime.now()
greeting = get_greeting(current_time)
print(f"Текущее время: {current_time}, Приветствие: {greeting}")

# Вывод данных о картах
print("Данные о картах:")
for card in get_card_data():
    print(
        f"Последние 4 цифры карты: {card['last_digits']}, Общая сумма расходов: {card['total_spent']}, "
        f"Кешбэк: {card['cashback']}"
    )

# Вывод топ-5 транзакций
print("\nТоп-5 транзакций:")
for transaction in get_top_transactions():
    print(
        f"Дата: {transaction['date']}, Сумма: {transaction['amount']}, Категория: {transaction['category']}, "
        f"Описание: {transaction['description']}"
    )

# Вывод курсов валют
print("\nКурс валют:")
currency_rates = get_currency_rates()
for rate in currency_rates:
    print(f"Валюта: {rate['currency']}, Курс: {rate['rate']}")

# Вывод стоимости акций
print("\nСтоимость акций из S&P500:")
stock_prices = get_stock_prices()
for stock in stock_prices:
    print(f"Акция: {stock['stock']}, Цена: {stock['price']}")
