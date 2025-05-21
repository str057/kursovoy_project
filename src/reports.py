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
        datetime(2021, 12, 31) if date is None else datetime.strptime(date, "%Y-%m-%d")
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


if __name__ == "__main__":
    try:
        # Чтение файла Excel без жёсткого указания формата даты
        transactions_df = pd.read_excel(
            Path("C:/Users/R/PycharmProjects/kr/data/operations.xlsx")
        )

        # Преобразование колонки 'Дата операции' в datetime, с заменой некорректных значений на NaT
        transactions_df["Дата операции"] = pd.to_datetime(
            transactions_df["Дата операции"],
            format="%d.%m.%Y %H:%M:%S",
            errors="coerce",
            dayfirst=True,
        )

        # Проверка на наличие некорректных дат
        if transactions_df["Дата операции"].isnull().any():
            logging.error(
                "Ошибка: Некоторые значения в колонке 'Дата операции' не были преобразованы в datetime. Проверьте данные в файле 'operations.xlsx'."
            )
            exit(1)
    except FileNotFoundError as e:
        logging.error(f"Ошибка: файл 'operations.xlsx' не найден. {e}")
        exit(1)
    except Exception as e:
        logging.error(f"Произошла ошибка при чтении файла: {e}")
        exit(1)

        # Проверка наличия обязательных колонок
    required_columns = {
        "Категория",
        "Дата операции",
        "Сумма операции с округлением",
    }
    missing_columns = required_columns - set(transactions_df.columns)
    if missing_columns:
        logging.error(f"Ошибка: В файле отсутствуют колонки: {missing_columns}")
        exit(1)
    # Проверка, что колонка 'Дата операции' имеет тип datetime
    if not pd.api.types.is_datetime64_any_dtype(transactions_df["Дата операции"]):
        logging.error("Ошибка: Колонка 'Дата операции' не преобразована в datetime")
        exit(1)
    # Пример вызова функции с категорией "Супермаркеты"
    category_name = "Супермаркеты"
    result = spending_by_category(transactions_df, category_name)
    print(result.to_string(index=False))
