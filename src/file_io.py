"""
Модуль для чтения финансовых транзакций из CSV и Excel файлов.
"""

from typing import Any, Dict, List

import pandas as pd


def read_transactions_from_csv(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает CSV-файл с транзакциями и возвращает список словарей.
    """
    try:
        df = pd.read_csv(file_path)
        # Преобразуем DataFrame в список словарей
        return df.to_dict(orient="records")  # type: ignore[return-value]
    except (FileNotFoundError, PermissionError, pd.errors.EmptyDataError, ValueError, OSError):
        return []


def read_transactions_from_excel(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает Excel-файл (.xlsx) с транзакциями и возвращает список словарей.
    """
    try:
        df = pd.read_excel(file_path)
        return df.to_dict(orient="records")  # type: ignore[return-value]
    except (FileNotFoundError, PermissionError, ValueError, OSError):
        return []
