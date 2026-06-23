"""
Вспомогательные функции для работы с данными.
"""

import json
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd


def get_transactions_from_json(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON-файл с транзакциями и возвращает список словарей.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []


def read_transactions_from_excel(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает Excel-файл с транзакциями и возвращает список словарей.
    """
    try:
        df = pd.read_excel(file_path)
        df = df.where(pd.notnull(df), None)
        result = df.to_dict(orient="records")  # type: ignore
        # Замена nan на None
        for row in result:
            for k, v in row.items():
                if isinstance(v, float) and pd.isna(v):
                    row[k] = None
        return result  # type: ignore
    except (FileNotFoundError, PermissionError, ValueError, OSError):
        return []


def filter_transactions_by_date_range(transactions: List[Dict[str, Any]], target_date: str) -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции с начала месяца по указанную дату.
    """
    if not transactions:
        return []
    target_dt = datetime.strptime(target_date, "%Y-%m-%d")
    start_of_month = target_dt.replace(day=1)
    filtered = []
    for tx in transactions:
        date_str = tx.get("Дата операции")
        if not date_str:
            continue
        try:
            if isinstance(date_str, datetime):
                tx_date = date_str
            else:
                tx_date = datetime.strptime(str(date_str), "%Y-%m-%d")
        except ValueError:
            try:
                tx_date = datetime.strptime(str(date_str), "%d.%m.%Y")
            except ValueError:
                continue
        if start_of_month <= tx_date <= target_dt:
            filtered.append(tx)
    return filtered
