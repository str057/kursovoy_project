from datetime import datetime
from src.utils import (
    get_greeting,
    get_card_data,
    get_top_transactions,
    get_currency_rates,
    get_stock_prices,
)
def main_function(date_time_str):
    current_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
    greeting = get_greeting(current_time)
    cards = get_card_data()
    top_transactions = get_top_transactions()
    currency_rates = get_currency_rates()
    stock_prices = get_stock_prices()
    response = {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }
    return response  # Возвращаем response
if __name__ == "__main__":
    sample_date_time = "2024-06-01 12:00:00"
    result = main_function(sample_date_time)
    print(result)