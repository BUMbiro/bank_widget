"""Тесты для модуля generators."""

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def transactions():
    """Фикстура со списком транзакций (как в задании)."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод с карты на карту",
        },
    ]


# --------------------- filter_by_currency ---------------------
def test_filter_by_currency_usd(transactions):
    """Проверяем, что фильтрация по USD работает."""
    usd_filter = filter_by_currency(transactions, "USD")
    first = next(usd_filter)
    assert first["id"] == 939719570
    second = next(usd_filter)
    assert second["id"] == 142264268
    third = next(usd_filter)
    assert third["id"] == 895315941
    # Четвёртого нет – должен быть StopIteration
    with pytest.raises(StopIteration):
        next(usd_filter)


def test_filter_by_currency_rub(transactions):
    """Проверяем фильтрацию по RUB."""
    rub_filter = filter_by_currency(transactions, "RUB")
    first = next(rub_filter)
    assert first["id"] == 873106923
    with pytest.raises(StopIteration):
        next(rub_filter)


def test_filter_by_currency_no_match(transactions):
    """Если нет транзакций с такой валютой, итератор пуст."""
    eur_filter = filter_by_currency(transactions, "EUR")
    with pytest.raises(StopIteration):
        next(eur_filter)


def test_filter_by_currency_empty_list():
    """Пустой список транзакций – итератор сразу пуст."""
    empty_filter = filter_by_currency([], "USD")
    with pytest.raises(StopIteration):
        next(empty_filter)


# --------------------- transaction_descriptions ---------------------
def test_transaction_descriptions(transactions):
    """Проверяем, что генератор выдаёт правильные описания."""
    descriptions = transaction_descriptions(transactions)
    assert next(descriptions) == "Перевод организации"
    assert next(descriptions) == "Перевод со счета на счет"
    assert next(descriptions) == "Перевод со счета на счет"
    assert next(descriptions) == "Перевод с карты на карту"
    with pytest.raises(StopIteration):
        next(descriptions)


def test_transaction_descriptions_empty():
    """Пустой список – генератор сразу завершается."""
    desc = transaction_descriptions([])
    with pytest.raises(StopIteration):
        next(desc)


# --------------------- card_number_generator ---------------------
@pytest.mark.parametrize(
    "start, stop, expected",
    [
        (
            1,
            5,
            [
                "0000 0000 0000 0001",
                "0000 0000 0000 0002",
                "0000 0000 0000 0003",
                "0000 0000 0000 0004",
                "0000 0000 0000 0005",
            ],
        ),
        (9999999999999999, 9999999999999999, ["9999 9999 9999 9999"]),
        (0, 0, ["0000 0000 0000 0000"]),
        (10, 12, ["0000 0000 0000 0010", "0000 0000 0000 0011", "0000 0000 0000 0012"]),
    ],
)
def test_card_number_generator_parametrized(start, stop, expected):
    """Проверяем генератор номеров карт с разными диапазонами."""
    result = list(card_number_generator(start, stop))
    assert result == expected


def test_card_number_generator_format():
    """Проверяем форматирование одного номера."""
    gen = card_number_generator(1234567890123456, 1234567890123456)
    assert next(gen) == "1234 5678 9012 3456"
