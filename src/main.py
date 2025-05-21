import json
import logging
import requests
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from services import analyze_cashback_from_excel  # Импортируем функцию из services.py

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
API_KEY = "3shKU2HqiqthC9VwyFJwUsTGZSuBKqclea"


def get_greeting(now):
    if now.hour < 6:
        return "Доброй ночи"
    if now.hour < 12:
        return "Доброе утро"
    if now.hour < 18:
        return "Добрый день"
    return "Добрый вечер"


def get_card_data():
    cards = [
        {"last_digits": "5814", "total_spent": 1262},
        {"last_digits": "7512", "total_spent": 7.94},
    ]
    for c in cards:
        c["cashback"] = round(c["total_spent"] / 100, 2)
    return cards


def get_top_transactions():
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
    return sorted(transactions, key=lambda x: x["amount"], reverse=True)


def get_currency_rates():
    url = f"https://api.exchangerate-api.com/v4/latest/USD?apikey={API_KEY}"
    rates = requests.get(url).json().get("rates", {})
    return [{"currency": k, "rate": v} for k, v in rates.items()]


def get_stock_prices():
    stocks = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    prices = []
    for s in stocks:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={s}&apikey={API_KEY}"
        r = requests.get(url).json()
        try:
            last_refreshed = r["Meta Data"]["3. Last Refreshed"]
            price = r["Time Series (Daily)"][last_refreshed]["4. close"]
            prices.append({"stock": s, "price": float(price)})
        except KeyError:
            prices.append({"stock": s, "price": None})
    return prices


def spending_by_category(transactions, category, date=None):
    date = datetime(2021, 12, 31) if not date else datetime.strptime(date, "%Y-%m-%d")
    three_months_ago = date - timedelta(days=90)
    df = transactions[
        (transactions["Категория"] == category)
        & (transactions["Дата операции"] >= three_months_ago)
        & (transactions["Дата операции"] <= date)
    ]
    total = df["Сумма операции с округлением"].sum()
    logging.info(
        f"Траты по категории '{category}' с {three_months_ago.date()} по {date.date()}: {total:.2f}"
    )
    return {"category": category, "total_spent": total}


def main():
    now = datetime.now()
    greeting = get_greeting(now)
    logging.info(f"{greeting}, текущее время: {now}")

    # Сбор данных для JSON
    output_data = {
        "greeting": greeting,
        "current_time": now.isoformat(),
        "cards": get_card_data(),
        "top_transactions": get_top_transactions(),
        "currency_rates": get_currency_rates(),
        "stock_prices": get_stock_prices(),
    }
    # Чтение данных из Excel и расчет трат по категории
    try:
        file_path = Path("C:/Users/R/PycharmProjects/kr/data/operations.xlsx")
        df = pd.read_excel(file_path)
        df["Дата операции"] = pd.to_datetime(
            df["Дата операции"], dayfirst=True, errors="coerce"
        )
        # Проверка на наличие некорректных дат
        if df["Дата операции"].isnull().any():
            logging.error("Некорректные даты в 'Дата операции'.")
            return
        # Анализ кешбэка с помощью функции из services.py
        year = 2021
        month = 12
        cashback_analysis = analyze_cashback_from_excel(file_path, year, month)
        output_data["cashback_analysis"] = cashback_analysis
    except Exception as e:
        logging.error("Ошибка при работе с Excel: %s", e)
    # Вывод результата в формате JSON
    json_result = json.dumps(output_data, ensure_ascii=False, indent=4)
    print(json_result)
    # Сохраняем в файл
    with open("output.json", "w", encoding="utf-8") as f:
        f.write(json_result)


if __name__ == "__main__":
    main()
