import pandas as pd
from datetime import datetime, timedelta
from typing import Optional
import logging
from pathlib import Path

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
    filtered_transactions = transactions[
        (transactions["category"] == category)
        & (transactions["date"] >= three_months_ago)
        & (transactions["date"] <= processing_date)
    ]
    total_spending = filtered_transactions["amount"].sum()
    logging.info(
        'Total spending for category "%s" from %s to %s: %.2f',
        category,
        three_months_ago.date(),
        processing_date.date(),
        total_spending,
    )
    return pd.DataFrame({"category": [category], "total_spending": [total_spending]})


if __name__ == "__main__":
    try:
        # Чтение файла Excel без жёсткого указания формата даты
        transactions_df = pd.read_excel(Path("food.xlsx"))
        # Преобразование колонки 'date' в datetime, с заменой некорректных значений на NaT
        transactions_df["date"] = pd.to_datetime(
            transactions_df["date"], errors="coerce"
        )
        # Проверка на наличие некорректных дат
        if transactions_df["date"].isnull().any():
            logging.error(
                "Ошибка: Некоторые значения в колонке 'date' не были преобразованы в datetime. Проверьте данные в файле 'food.xlsx'."
            )
            exit(1)
    except FileNotFoundError as e:
        logging.error(f"Ошибка: файл 'food.xlsx' не найден. {e}")
        exit(1)
    except Exception as e:
        logging.error(f"Произошла ошибка при чтении файла: {e}")
        exit(1)
        # Проверка наличия обязательных колонок
    required_columns = {"category", "date", "amount"}
    missing_columns = required_columns - set(transactions_df.columns)
    if missing_columns:
        logging.error(f"Ошибка: В файле отсутствуют колонки: {missing_columns}")
        exit(1)
    # Проверка, что колонка 'date' имеет тип datetime
    if not pd.api.types.is_datetime64_any_dtype(transactions_df["date"]):
        logging.error("Ошибка: Колонка 'date' не преобразована в datetime")
        exit(1)
    # Пример вызова функции с категорией "Молочные продукты"
    category_name = "Молочные продукты"
    result = spending_by_category(transactions_df, category_name)
    print(result)
