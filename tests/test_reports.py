import pandas as pd
from datetime import datetime, timedelta
from typing import Optional
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def spending_by_category(
    transactions: pd.DataFrame, category: str, date: Optional[str] = None
) -> pd.DataFrame:
    """
    Рассчитывает сумму трат по категории за последние 3 месяца от заданной даты (по умолчанию сегодня)
    """
    processing_date = (
        datetime.now() if date is None else datetime.strptime(date, "%Y-%m-%d")
    )
    three_months_ago = processing_date - timedelta(days=90)
    # Фильтрация транзакций по категории и дате
    filtered_transactions = transactions[
        (transactions["Категория"] == category)
        & (transactions["Дата операции"] >= three_months_ago)
        & (transactions["Дата операции"] <= processing_date)
    ]
    total_spending = filtered_transactions["Сумма операции с округлением"].sum()
    logging.info(
        'Total spending for category "%s" from %s to %s: %.2f',
        category,
        three_months_ago.date(),
        processing_date.date(),
        total_spending,
    )
    return pd.DataFrame({"category": [category], "total_spending": [total_spending]})
