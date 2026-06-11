"""
Вспомогательные функции для работы с данными.
Содержит функции для чтения JSON и Excel, фильтрации по дате.
"""

import json
import pandas as pd
from typing import List, Dict, Any
from datetime import datetime


# ----------------------- Работа с JSON -----------------------
def get_transactions_from_json(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON-файл с транзакциями и возвращает список словарей.

    Если файл не найден, пустой или содержимое не является списком,
    возвращает пустой список.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        else:
            return []
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []


# ----------------------- Работа с Excel -----------------------
def read_transactions_from_excel(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает Excel-файл с транзакциями и возвращает список словарей.

    Аргументы:
        file_path (str): путь к файлу .xlsx

    Возвращает:
        List[Dict[str, Any]]: список транзакций, где каждая транзакция — словарь.
    """
    try:
        df = pd.read_excel(file_path)
        # Заменяем NaN на None для корректного преобразования в JSON
        df = df.where(pd.notnull(df), None)
        # to_dict() возвращает List[Dict[Hashable, Any]], но мы знаем, что ключи — строки.
        # Добавляем type: ignore, чтобы mypy не ругался.
        return df.to_dict(orient='records')  # type: ignore[return-value]
    except Exception as e:
        print(f"Ошибка при чтении файла {file_path}: {e}")
        return []


def filter_transactions_by_date_range(transactions: List[Dict[str, Any]], target_date: str) -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции: оставляет только те, у которых дата операции попадает в период
    с начала месяца, на который выпадает target_date, по эту дату включительно.

    Аргументы:
        transactions (List[Dict[str, Any]]): список транзакций (должен содержать ключ 'Дата операции').
        target_date (str): строка в формате 'YYYY-MM-DD'.

    Возвращает:
        List[Dict[str, Any]]: отфильтрованный список транзакций.
    """
    if not transactions:
        return []

    target_dt = datetime.strptime(target_date, '%Y-%m-%d')
    start_of_month = target_dt.replace(day=1)
    filtered = []

    for tx in transactions:
        date_str = tx.get('Дата операции')
        if not date_str:
            continue
        try:
            # Если дата уже объект datetime (например, из pandas)
            if isinstance(date_str, datetime):
                tx_date = date_str
            else:
                tx_date = datetime.strptime(str(date_str), '%Y-%m-%d')
        except ValueError:
            # Пробуем альтернативный формат (день.месяц.год)
            try:
                tx_date = datetime.strptime(str(date_str), '%d.%m.%Y')
            except ValueError:
                continue
        if start_of_month <= tx_date <= target_dt:
            filtered.append(tx)
    return filtered
