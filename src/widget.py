"""Модуль для обработки строк с информацией о картах, счетах и датах."""

from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(info: str) -> str:
    """
    Принимает строку вида 'Visa Platinum 7000792289606361'
    или 'Счет 73654108430135874305' и возвращает строку с замаскированным номером.
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
    Принимает дату в ISO-формате (2024-03-11T02:26:18.671407)
    и возвращает в формате ДД.ММ.ГГГГ (11.03.2024).
    """
    dt = datetime.fromisoformat(date_string)
    return dt.strftime("%d.%m.%Y")
