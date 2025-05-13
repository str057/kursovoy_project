import json
import pandas as pd
import logging
from typing import List, Dict

# Настройка логирования
logging.basicConfig(level=logging.INFO)


def load_cashback_data_from_excel(file_path: str) -> List[Dict]:
    """
    Загружает данные о кешбэке из Excel-файла.
    Предполагается, что файл содержит столбцы:
    - 'date' (дата транзакции в формате ГГГГ-ММ-ДД)
    - 'category' (категория транзакции)
    - 'cashback' (сумма кешбэка в числовом формате)    :param file_path: Путь к Excel-файлу.
    :return: Список транзакций в формате словарей.
    """
    df = pd.read_excel(file_path)
    # Проверяем, что необходимые столбцы есть в файле
    required_cols = {"date", "category", "cashback"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"В файле отсутствуют необходимые столбцы: {required_cols}")

    # Преобразуем данные в список словарей
    data = df.to_dict(orient="records")
    return data


def analyze_cashback_categories(
    data: List[Dict], year: int, month: int, output_file: str
) -> None:
    """
    Анализирует, какие категории были наиболее выгодными для выбора в качестве категорий повышенного кешбэка
    и сохраняет результат в файл JSON.
    :param data: Список транзакций, где каждая транзакция представлена словарем.
    :param year: Год для анализа.
    :param month: Месяц для анализа.
    :param output_file: Путь к файлу, в который будет сохранен результат.
    """
    cashback_summary: Dict[str, int] = {}  # Добавлена аннотация типа
    for transaction in data:
        transaction_date = transaction["date"]  # Это уже Timestamp
        if transaction_date.year == year and transaction_date.month == month:
            category = transaction["category"]
            cashback_amount = transaction["cashback"]  # Суммируем кешбэк по категориям
            if category in cashback_summary:
                cashback_summary[category] += cashback_amount
            else:
                cashback_summary[category] = cashback_amount
    # Преобразование результата в JSON
    result_json = json.dumps(cashback_summary, ensure_ascii=False)
    logging.info("Анализ кешбэка завершен. Результат: %s", result_json)
    # Сохранение результата в файл
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(result_json)
    logging.info("Результат сохранен в файл: %s", output_file)


if __name__ == "__main__":
    excel_file = (
        r"C:\Users\R\PycharmProjects\kr\data\list_kshb.xlsx"  # Используйте сырую строку
    )
    year = 2023  # Год для анализа
    month = 10  # Месяц для анализа
    output_file = "cashback_result.json"  # Путь к выходному файлу
    try:
        # Загружаем данные из Excel
        data = load_cashback_data_from_excel(excel_file)
        # Анализируем кешбэк
        analyze_cashback_categories(data, year, month, output_file)
        print(f"Результаты анализа сохранены в файл {output_file}")
    except Exception as e:
        print(f"Ошибка при обработке данных: {e}")
