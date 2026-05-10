import pytest

from src.widget import get_date, mask_account_card


# ----- Фикстура для разных карт/счетов -----
@pytest.fixture
def card_account_strings():
    return {
        "visa": "Visa Platinum 7000792289606361",
        "maestro": "Maestro 1596837868705199",
        "account": "Счет 73654108430135874305",
    }


# ----- Тесты mask_account_card -----
def test_mask_account_card_card(card_account_strings):
    assert mask_account_card(card_account_strings["visa"]) == "Visa Platinum 7000 79** **** 6361"
    assert mask_account_card(card_account_strings["maestro"]) == "Maestro 1596 83** **** 5199"


def test_mask_account_card_account(card_account_strings):
    assert mask_account_card(card_account_strings["account"]) == "Счет **4305"


@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
    ],
)
def test_mask_account_card_parametrized(input_str, expected):
    assert mask_account_card(input_str) == expected


def test_mask_account_card_invalid_no_space():
    # если нет пробела – возвращает исходную строку
    assert mask_account_card("Некорректная строка") == "Некорректная строка"


# ----- Тесты get_date -----
def test_get_date_valid():
    assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"


@pytest.mark.parametrize(
    "date_str, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2025-12-31T23:59:59", "31.12.2025"),
        ("2000-01-01T00:00:00", "01.01.2000"),
    ],
)
def test_get_date_parametrized(date_str, expected):
    assert get_date(date_str) == expected


def test_get_date_iso_without_time():
    # некоторые строки могут быть без времени
    assert get_date("2024-03-11") == "11.03.2024"
