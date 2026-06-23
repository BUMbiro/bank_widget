"""
Модуль с сервисами: выгодные категории кешбэка, поиск по телефонным номерам, инвесткопилка.
"""

import re
from collections import Counter
from datetime import datetime
from typing import Any, Dict, List


def profitable_cashback_categories(transactions: List[Dict[str, Any]], year: int, month: int) -> Dict[str, float]:
    """
    Анализирует, сколько кешбэка можно получить по каждой категории за указанный месяц.
    """
    filtered = []
    for tx in transactions:
        date_str = tx.get("Дата операции")
        if not date_str:
            continue
        try:
            if isinstance(date_str, datetime):
                dt = date_str
            else:
                dt = datetime.strptime(str(date_str), "%Y-%m-%d")
        except (ValueError, TypeError):
            continue
        if dt.year == year and dt.month == month:
            filtered.append(tx)

    category_spent: Counter = Counter()  # аннотация типа
    for tx in filtered:
        amount = tx.get("Сумма операции", 0)
        if amount > 0:  # расходы
            category = tx.get("Категория", "Без категории")
            category_spent[category] += amount
    cashback_by_category = {cat: spent / 100 for cat, spent in category_spent.items()}
    return {cat: round(val, 2) for cat, val in cashback_by_category.items()}


def search_by_phone_numbers(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Возвращает транзакции, в описании которых встречается российский мобильный номер.
    """
    result = []
    for tx in transactions:
        desc = tx.get("Описание", "")
        # Извлекаем все цифры из описания
        digits = re.sub(r"\D", "", desc)
        # Проверяем, что последовательность начинается с 7 или 8 и имеет длину 10 или 11
        if len(digits) in (10, 11) and digits[0] in ("7", "8"):
            result.append(tx)
    return result


def investment_bank(transactions: List[Dict[str, Any]], month: str, limit: int = 50) -> float:
    """
    Рассчитывает сумму, которую удалось бы отложить в «Инвесткопилку» за указанный месяц.
    """
    year, mon = map(int, month.split("-"))
    total = 0.0
    for tx in transactions:
        date_str = tx.get("Дата операции")
        if not date_str:
            continue
        try:
            if isinstance(date_str, datetime):
                dt = date_str
            else:
                dt = datetime.strptime(str(date_str), "%Y-%m-%d")
        except (ValueError, TypeError):
            continue
        if dt.year == year and dt.month == mon:
            amount = tx.get("Сумма операции", 0)
            spent = abs(amount) if amount > 0 else 0
            if spent > 0:
                rounded = ((spent + limit - 1) // limit) * limit
                saved = rounded - spent
                total += saved
    return round(total, 2)


# Для самопроверки (можно удалить или оставить)
if __name__ == "__main__":
    from src.utils import read_transactions_from_excel

    data = read_transactions_from_excel("data/operations.xlsx")
    if data:
        print("Кешбэк за май 2020:", profitable_cashback_categories(data, 2020, 5))
        print("Телефоны:", len(search_by_phone_numbers(data)))
        print("Инвесткопилка за 2025-06 при limit=50:", investment_bank(data, "2025-06", 50))
