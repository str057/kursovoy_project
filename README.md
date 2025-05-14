# Project Bank
Приложение для анализа транзакций, которые находятся в Excel-файле. Приложение будет генерировать JSON-данные для веб-страниц, формировать Excel-отчеты, а также предоставлять другие сервисы.

## Описание

Проект состоит из следующих функций:

`def load_cashback_data_from_excel(file_path: str) -> List[Dict]:`: Загружает данные о кешбэке из Excel-файла.
-   `def analyze_cashback_categories`: Анализирует, какие категории были наиболее выгодными для выбора в качестве категорий повышенного кешбэка.
-   `def main_function`:  предназначена для обработки входной строки даты и времени, а затем для получения различных данных
-   `def load_currency_rates_from_file`: Эта функция предназначена для загрузки курсов валют из файла в формате JSON.
-   `def get_greeting`:Эта функция предназначена для генерации приветственного сообщения на основе текущего времени суток.
-   `def get_card_data()`: Функция предназначена для получения информации о картах пользователя, включая последние цифры карт, общую сумму расходов и начисленный кэшбэк.
-   `def get_top_transactions()`: Функция  предназначена для получения информации о значительных транзакциях пользователя.
-   `def get_currency_rates()`: Функция get_currency_rates предназначена для получения актуальных курсов валют с использованием API. 
-   `def get_stock_prices()`: Функция get_stock_prices предназначена для получения текущих цен акций определенных компаний с использованием API. 
-   `def spending_by_category(`: Рассчитывает сумму трат по категории за последние 3 месяца от заданной даты (по умолчанию сегодня)



## Установка

Для установки и запуска проекта необходимо выполнить следующие шаги:

1.  **Клонируйте репозиторий:**

    ```
    git clone https://github.com/str057/re_10_1.git
    ```

2.  **Перейдите в папку проекта:**

    ```
    kr
    ```

3.  **Установите зависимости с помощью Poetry:**

    ```
    poetry install
    ```

## Использование

Примеры использования функций:

~~~
from src.widget import get_mask_card_number, get_mask_account, mask_account_card, get_date, filter_by_state, sort_by_date
from typing import Dict, List

Маскировка номера карты
card_number = "6831982470375048"
masked_card = get_mask_card_number(card_number)
print(f"Masked card number: {masked_card}") # Output: 6831 98** **** 5048

Маскировка номера счета
account_number = "12345678901234567890"
masked_account = get_mask_account(account_number)
print(f"Masked account number: {masked_account}") # Output: **7890

Маскировка информации о карте/счете
bank_details = "Visa Classic 6831982470375048"
masked_details = mask_account_card(bank_details)
print(f"Masked details: {masked_details}") # Output: Visa Classic 6831 98** **** 5048


Пример данных для фильтрации и сортировки
transactions: List[Dict] = [
{"id": 1, "date": "2023-10-27T10:00:00", "state": "EXECUTED", "amount": 100},
{"id": 2, "date": "2023-10-26T12:00:00", "state": "CANCELED", "amount": 50},
{"id": 3, "date": "2023-10-28T14:00:00", "state": "EXECUTED", "amount": 200},
]

Фильтрация по статусу
executed_transactions = filter_by_state(transactions, state="EXECUTED")
print(f"Executed transactions: {executed_transactions}")

Сортировка по дате
sorted_transactions = sort_by_date(transactions)
print(f"Sorted transactions: {sorted_transactions}")

~~~
#######
## Зависимости

Проект использует следующие зависимости:

*   Python 3.12.4
*   Poetry (для управления зависимостями)


## Лицензия

Этот проект лицензирован по [лицензии MIT](LICENSE).

# Тестирование проекта

Этот проект включает в себя набор тестов, написанных с использованием
библиотеки [pytest](https://docs.pytest.org/en/stable/). Тесты помогают обеспечить 
корректность работы функций и модулей проекта.

## Структура тестов

Тесты организованы в папке `tests/`, где каждый файл соответствует модулю в проекте. Например:

## Описание тестов
Тесты для маскирования номера карты
Функция get_mask_card_number тестируется на различных входных данных, включая корректные и некорректные номера карт.

Тесты для фильтрации транзакций
Функция filter_by_state тестируется на различных состояниях транзакций, чтобы убедиться, что она правильно фильтрует
данные.

Тесты для сортировки транзакций
Функция sort_by_date тестируется на различных сценариях, включая сортировку по одинаковым датам и пустым спискам.

Тесты для виджетов
Функции mask_account_card и get_date тестируются на корректность маскирования и форматирования даты.