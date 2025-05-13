import json
import os
import logging
import requests
from datetime import datetime

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


API_KEY = os.getenv(
    "API_KEY", "3shKU2HqiqthC9VwyFJwUsTGZSuBKqclea"
)
if API_KEY is None:
    raise ValueError("API_KEY не установлен")

# функция предназначена для загрузки курсов валют из файла в формате JSON.
def load_currency_rates_from_file():
    with open("glavnaya.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        return data.get("rates", {})

# функция предназначена для генерации приветственного сообщения на основе текущего времени суток.
def get_greeting(current_time):
    if current_time.hour < 6:
        return "Доброй ночи"
    elif current_time.hour < 12:
        return "Доброе утро"
    elif current_time.hour < 18:
        return "Добрый день"
    else:
        return "Добрый вечер"

# Функция предназначена для получения информации о картах пользователя, включая последние цифры карт,
# общую сумму расходов и начисленный кэшбэк
def get_card_data():
    # Пример данных о картах
    cards = [
        {"last_digits": "5814", "total_spent": 1262.00},
        {"last_digits": "7512", "total_spent": 7.94},
    ]
    for card in cards:
        card["cashback"] = round(card["total_spent"] / 100, 2)
    return cards

#Функция  предназначена для получения информации о значительных транзакциях пользователя.
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
    stocks = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    prices = {}
    for stock in stocks:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}&apikey={API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            try:
                last_refreshed = data["Meta Data"]["3. Last Refreshed"]
                current_price = data["Time Series (Daily)"][last_refreshed]["4. close"]
                prices[stock] = current_price
            except KeyError:
                prices[stock] = None  # Если данные недоступны
        else:
            prices[stock] = None  # Если запрос не удался
    return [
        {"stock": stock, "price": prices[stock] if prices[stock] is not None else "N/A"}
        for stock in stocks
    ]


current_time = datetime.now()
greeting = get_greeting(current_time)

logging.info(f"Текущее время: {current_time}, Приветствие: {greeting}")
# Вывод данных о картах
logging.info("Данные о картах:")
for card in get_card_data():
    logging.info(
        f"Последние 4 цифры карты: {card['last_digits']}, Общая сумма расходов: {card['total_spent']}, "
        f"Кешбэк: {card['cashback']}"
    )


# Вывод топ-5 транзакций
logging.info("\nТоп-5 транзакций:")
for transaction in get_top_transactions():
    logging.info(
        f"Дата: {transaction['date']}, Сумма: {transaction['amount']}, Категория: {transaction['category']}, "
        f"Описание: {transaction['description']}"
    )
# Вывод курсов валют
logging.info("\nКурс валют:")
currency_rates = get_currency_rates()
for rate in currency_rates:
    logging.info(f"Валюта: {rate['currency']}, Курс: {rate['rate']}")
# Вывод стоимости акций
logging.info("\nСтоимость акций из S&P500:")
stock_prices = get_stock_prices()
for stock in stock_prices:
    logging.info(f"Акция: {stock['stock']}, Цена: {stock['price']}")
