"""
Главный модуль приложения для работы с банковскими транзакциями.
"""

from typing import List, Dict, Any

# Импорт существующих функций
from src.utils import get_transactions_from_json
from src.file_io import read_transactions_from_csv, read_transactions_from_excel
from src.processing import filter_by_state, sort_by_date
from src.widget import get_date, mask_account_card
from src.search_utils import search_transactions


def load_transactions(source: int) -> List[Dict[str, Any]]:
    """Загружает транзакции из выбранного источника."""
    if source == 1:
        file_path = "data/operations.json"
        print("Для обработки выбран JSON-файл.")
        return get_transactions_from_json(file_path)
    elif source == 2:
        file_path = "data/transactions.csv"
        print("Для обработки выбран CSV-файл.")
        return read_transactions_from_csv(file_path)
    elif source == 3:
        file_path = "data/transactions.xlsx"
        print("Для обработки выбран XLSX-файл.")
        return read_transactions_from_excel(file_path)
    else:
        print("Неверный выбор. Будет использован JSON-файл по умолчанию.")
        return get_transactions_from_json("data/operations.json")


def get_valid_status() -> str:
    """Запрашивает статус, пока не будет введён корректный."""
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        status = input(
            "Введите статус, по которому необходимо выполнить фильтрацию.\n"
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n"
        ).strip().upper()
        if status in valid_statuses:
            print(f'Операции отфильтрованы по статусу "{status}"')
            return status
        else:
            print(f'Статус операции "{status}" недоступен.')


def get_boolean_input(prompt: str) -> bool:
    """Запрашивает Да/Нет, возвращает True/False."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("да", "yes", "y", "д"):
            return True
        if answer in ("нет", "no", "n", "н"):
            return False
        print("Пожалуйста, ответьте 'Да' или 'Нет'.")


def get_sort_order() -> bool:
    """Запрашивает направление сортировки. Возвращает True для убывания, False для возрастания."""
    while True:
        order = input("Отсортировать по возрастанию или по убыванию? ").strip().lower()
        if order in ("по убыванию", "убывание", "desc", "убыв"):
            return True   # descending
        if order in ("по возрастанию", "возрастание", "asc", "возр"):
            return False  # ascending
        print("Введите 'по возрастанию' или 'по убыванию'.")


def display_transactions(transactions: List[Dict[str, Any]]) -> None:
    """Выводит транзакции в форматированном виде."""
    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return
    print(f"Всего банковских операций в выборке: {len(transactions)}")
    for tx in transactions:
        date_str = tx.get("date", "")
        formatted_date = get_date(date_str) if date_str else "Дата не указана"
        description = tx.get("description", "")
        from_acc = tx.get("from", "")
        to_acc = tx.get("to", "")
        amount = tx.get("operationAmount", {}).get("amount", "0")
        currency = tx.get("operationAmount", {}).get("currency", {}).get("code", "RUB")

        print(f"\n{formatted_date} {description}")
        if from_acc and to_acc:
            from_masked = mask_account_card(from_acc) if " " in from_acc else from_acc
            to_masked = mask_account_card(to_acc) if " " in to_acc else to_acc
            print(f"{from_masked} -> {to_masked}")
        elif from_acc:
            print(f"Счёт {from_acc}")
        elif to_acc:
            print(f"Счёт {to_acc}")
        print(f"Сумма: {amount} {currency}")
    print()


def main() -> None:
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")
    choice = input().strip()
    while choice not in ('1', '2', '3'):
        print("Пожалуйста, выберите 1, 2 или 3.")
        choice = input().strip()
    transactions = load_transactions(int(choice))
    if not transactions:
        print("Не удалось загрузить транзакции. Завершение работы.")
        return

    status = get_valid_status()
    filtered = filter_by_state(transactions, status)

    if get_boolean_input("Отсортировать операции по дате? Да/Нет\n"):
        descending = get_sort_order()
        filtered = sort_by_date(filtered, descending=descending)

    if get_boolean_input("Выводить только рублевые транзакции? Да/Нет\n"):
        filtered = [tx for tx in filtered
                    if tx.get("operationAmount", {}).get("currency", {}).get("code") == "RUB"]

    if get_boolean_input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n"):
        search_word = input("Введите слово или фразу для поиска: ").strip()
        if search_word:
            filtered = search_transactions(filtered, search_word)

    print("Распечатываю итоговый список транзакций...")
    display_transactions(filtered)


if __name__ == "__main__":
    main()
