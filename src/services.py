import json
import pandas as pd
from typing import Dict


def analyze_cashback_from_excel(
    file_path: str, year: int, month: int, top_n: int = 5
) -> Dict[str, float]:
    # Чтение Excel
    df = pd.read_excel(file_path)
    # Проверяем наличие нужных столбцов
    required_cols = {"Дата операции", "Категория", "Кэшбэк"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"Отсутствуют столбцы в Excel: {required_cols}")
    # Парсим даты с нужным форматом
    df["Дата операции"] = pd.to_datetime(
        df["Дата операции"], format="%d.%m.%Y %H:%M:%S"
    )
    # Фильтруем по году и месяцу
    df_filtered = df[
        (df["Дата операции"].dt.year == year) & (df["Дата операции"].dt.month == month)
    ]

    # Группируем по категориям и суммируем кешбэк
    summary = df_filtered.groupby("Категория")["Кэшбэк"].sum()
    # Преобразуем в словарь с округлением до 2 знаков
    result = {cat: round(amount, 2) for cat, amount in summary.items()}
    # Сортируем и выбираем только топ-N категорий
    top_categories = dict(
        sorted(result.items(), key=lambda item: item[1], reverse=True)[:top_n]
    )
    return top_categories


if __name__ == "__main__":
    file_path = r"C:\Users\R\PycharmProjects\kr\data\operations.xlsx"
    year = 2021
    month = 12
    # Получаем результат анализа кешбэка
    result = analyze_cashback_from_excel(file_path, year, month)
    # Вывод результата в формате JSON
    json_result = json.dumps(result, ensure_ascii=False, indent=4)
    print(json_result)
    # Сохраняем в файл
    with open("cashback_summary.json", "w", encoding="utf-8") as f:
        f.write(json_result)
