import pytest

from src.masks import get_mask_account, get_mask_card_number


# ---------- Фикстуры для данных ----------
@pytest.fixture
def valid_card_numbers():
    return [7000792289606361, 1234567890123456]


@pytest.fixture
def valid_account_numbers():
    return [73654108430135874305, 12345678901234567890]


# ---------- Тесты для get_mask_card_number ----------
def test_get_mask_card_number_valid():
    assert get_mask_card_number(7000792289606361) == "7000 79** **** 6361"
    assert get_mask_card_number(1234567890123456) == "1234 56** **** 3456"


@pytest.mark.parametrize(
    "card_number, expected",
    [
        (7000792289606361, "7000 79** **** 6361"),
        (1234567890123456, "1234 56** **** 3456"),
        (1111222233334444, "1111 22** **** 4444"),
    ],
)
def test_get_mask_card_number_parametrized(card_number, expected):
    assert get_mask_card_number(card_number) == expected


def test_get_mask_card_number_invalid_too_short():
    # функция не проверяет длину, но для теста просто убедимся, что нет ошибки
    assert get_mask_card_number(12345) == "1234 5** **** 2345"  # на выходе будут странные звезды, но это допустимо


# ---------- Тесты для get_mask_account ----------
def test_get_mask_account_valid():
    assert get_mask_account(73654108430135874305) == "**4305"
    assert get_mask_account(12345678901234567890) == "**7890"


@pytest.mark.parametrize(
    "account_number, expected",
    [
        (73654108430135874305, "**4305"),
        (98765432109876543210, "**3210"),
    ],
)
def test_get_mask_account_parametrized(account_number, expected):
    assert get_mask_account(account_number) == expected


def test_get_mask_account_short():
    # даже если номер короткий, получим последние 4 символа
    assert get_mask_account(12345) == "**2345"
