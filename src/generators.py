"""Модуль с генераторами для обработки транзакций."""

from typing import Any, Dict, Iterator, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str) -> Iterator[Dict[str, Any]]:
    """
    Принимает список транзакций и код валюты.
    Возвращает итератор, который выдаёт транзакции с указанной валютой.
    """
    for transaction in transactions:
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency_code:
            yield transaction


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """
    Принимает список транзакций.
    Генерирует описание каждой транзакции по очереди.
    """
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """
    Генерирует номера банковских карт в заданном диапазоне.
    Каждый номер форматируется как "XXXX XXXX XXXX XXXX".
    """
    for number in range(start, stop + 1):
        # Форматируем число в строку с ведущими нулями до 16 цифр
        card_str = f"{number:016d}"
        # Разбиваем на группы по 4 цифры
        formatted = " ".join([card_str[i : i + 4] for i in range(0, 16, 4)])
        yield formatted
