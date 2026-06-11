"""
Модуль для формирования отчетов: траты по категории, декоратор для сохранения в файл.
"""

import json
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime, timedelta
from functools import wraps


def report_to_file(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для сохранения результата функции (словаря) в JSON-файл.
    Если filename не задан, имя генерируется автоматически.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            if filename is None:
                current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
                out_filename = f"{func.__name__}_{current_time}.json"
            else:
                out_filename = filename
            with open(out_filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False, default=str)
            return result
        return wrapper
    return decorator


@report_to_file()
def spending_by_category(
    transactions: List[Dict[str, Any]],
    category: str,
    date: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Возвращает траты по заданной категории за последние три месяца (от указанной даты).
    Если date не передана, берётся текущая дата.
    """
    if date is None:
        end_date = datetime.now()
    else:
        end_date = datetime.strptime(date, '%Y-%m-%d')
    start_date = end_date - timedelta(days=90)

    filtered = []
    for tx in transactions:
        date_str = tx.get('Дата операции')
        if not date_str:
            continue
        try:
            if isinstance(date_str, datetime):
                tx_date = date_str
            else:
                tx_date = datetime.strptime(str(date_str), '%Y-%m-%d')
        except ValueError:
            continue
        if start_date <= tx_date <= end_date:
            tx_category = tx.get('Категория', '')
            if tx_category.lower() == category.lower():
                filtered.append(tx)
    return filtered
