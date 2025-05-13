import pandas as pd
from datetime import datetime, timedelta
import pytest
from src.reports import spending_by_category
from freezegun import freeze_time


@pytest.fixture
def sample_transactions():
    base_date = datetime(2024, 6, 15)
    data = {
        "category": [
            "Молочные продукты",
            "Молочные продукты",
            "Фрукты",
            "Молочные продукты",
        ],
        "date": [
            base_date - timedelta(days=10),
            base_date - timedelta(days=100),
            base_date - timedelta(days=5),
            base_date - timedelta(days=20),
        ],
        "amount": [100.0, 200.0, 50.0, 150.0],
    }
    df = pd.DataFrame(data)
    return df


def test_spending_correct_sum(sample_transactions):
    # Считаем трату за 3 месяца с 2024-06-15 по умолчанию
    result = spending_by_category(
        sample_transactions, "Молочные продукты", date="2024-06-15"
    )
    assert not result.empty
    # За последние 90 дней 2 транзакции: 100 + 150 = 250
    assert result.loc[0, "total_spending"] == 250.0
    assert result.loc[0, "category"] == "Молочные продукты"


def test_spending_no_transactions(sample_transactions):
    # Категория отсутствует в данных
    result = spending_by_category(sample_transactions, "Мясо", date="2024-06-15")
    assert result.loc[0, "total_spending"] == 0.0
    assert result.loc[0, "category"] == "Мясо"


@freeze_time("2024-06-15")
def test_spending_with_current_date(sample_transactions):
    # Проверка работы с date=None - используется текущая дата
    result = spending_by_category(sample_transactions, "Фрукты", date=None)
    assert result.loc[0, "total_spending"] == 50.0

def test_spending_empty_dataframe():
    empty_df = pd.DataFrame(columns=["category", "date", "amount"])
    result = spending_by_category(empty_df, "Молочные продукты", date="2024-06-15")
    assert result.loc[0, "total_spending"] == 0.0
    assert result.loc[0, "category"] == "Молочные продукты"
