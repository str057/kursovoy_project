import json
import os
from datetime import datetime
from typing import List, Dict


def analyze_cashback_categories(
    data: List[Dict], year: int, month: int, output_file: str
) -> None:
    cashback_summary: Dict[str, float] = {}  # Type annotation added here
    for transaction in data:
        transaction_date = transaction["date"]
        if transaction_date.year == year and transaction_date.month == month:
            category = transaction["category"]
            cashback_amount = transaction["cashback"]
            if category in cashback_summary:
                cashback_summary[category] += cashback_amount
            else:
                cashback_summary[category] = cashback_amount
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(json.dumps(cashback_summary, ensure_ascii=False))


def test_cashback_simple():
    data = [
        {"date": datetime(2023, 10, 5), "category": "Food", "cashback": 2},
        {"date": datetime(2023, 10, 15), "category": "Food", "cashback": 3},
        {"date": datetime(2023, 9, 10), "category": "Transport", "cashback": 1},
    ]
    output_file = "test_output.json"
    analyze_cashback_categories(data, 2023, 10, output_file)
    with open(output_file, "r", encoding="utf-8") as f:
        result = json.load(f)
    assert result == {"Food": 5}
    os.remove(output_file)


if __name__ == "__main__":
    test_cashback_simple()
    print("Simple test passed.")
