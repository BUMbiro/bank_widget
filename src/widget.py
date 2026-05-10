"""
Модуль для обработки строк с информацией о картах и счетах.
"""

import datetime
from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(info: str) -> str:
    """
    Маскирует номер банковской карты или счета.
    """
    parts = info.rsplit(" ", 1)
    if len(parts) != 2:
        return info
    name, number = parts
    if not number.isdigit():
        return info
    if name.lower().startswith("счет"):
        return f"{name} {get_mask_account(int(number))}"
    else:
        return f"{name} {get_mask_card_number(int(number))}"


def get_date(date_string: str) -> str:
    """
    Преобразует ISO-строку в формат ДД.ММ.ГГГГ.
    """
    dt = datetime.datetime.fromisoformat(date_string)
    return dt.strftime("%d.%m.%Y")
