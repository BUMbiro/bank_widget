from src.services import (
    profitable_cashback_categories,
    search_by_phone_numbers,
    investment_bank
)


def test_profitable_cashback_categories():
    data = [
        {'Дата операции': '2020-05-15', 'Сумма операции': 200, 'Категория': 'Еда'},
        {'Дата операции': '2020-05-20', 'Сумма операции': 300, 'Категория': 'Еда'},
        {'Дата операции': '2020-05-25', 'Сумма операции': 500, 'Категория': 'Транспорт'},
        {'Дата операции': '2020-06-01', 'Сумма операции': 100, 'Категория': 'Еда'},
    ]
    result = profitable_cashback_categories(data, 2020, 5)
    assert result['Еда'] == (200 + 300) / 100
    assert result['Транспорт'] == 5.0


def test_profitable_cashback_categories_empty():
    assert profitable_cashback_categories([], 2020, 5) == {}


def test_profitable_cashback_categories_no_matching_month():
    data = [{'Дата операции': '2020-05-15', 'Сумма операции': 100, 'Категория': 'Еда'}]
    result = profitable_cashback_categories(data, 2021, 5)
    assert result == {}


def test_search_by_phone_numbers():
    data = [
        {'Описание': 'МТС +7 921 11-22-33'},
        {'Описание': 'Т-Банк Мобайл +7 995 555-55-55'},
        {'Описание': 'Просто текст без телефона'},
        {'Описание': 'Позвони 8-921-111-22-33'}
    ]
    result = search_by_phone_numbers(data)
    assert len(result) == 3


def test_search_by_phone_numbers_empty():
    assert search_by_phone_numbers([]) == []


def test_search_by_phone_numbers_no_match():
    data = [{'Описание': 'Обычный текст'}]
    assert search_by_phone_numbers(data) == []


def test_investment_bank():
    data = [
        {'Дата операции': '2025-06-10', 'Сумма операции': 1712},
        {'Дата операции': '2025-06-15', 'Сумма операции': 50},
        {'Дата операции': '2025-06-20', 'Сумма операции': 30},
        {'Дата операции': '2025-05-20', 'Сумма операции': 1000},
    ]
    result = investment_bank(data, '2025-06', limit=50)
    assert result == 38.0 + 0.0 + 20.0


def test_investment_bank_no_transactions():
    assert investment_bank([], '2025-06', 50) == 0.0


def test_investment_bank_different_limits():
    data = [{'Дата операции': '2025-06-10', 'Сумма операции': 1712}]
    assert investment_bank(data, '2025-06', limit=10) == (1720 - 1712)
    assert investment_bank(data, '2025-06', limit=100) == (1800 - 1712)


def test_investment_bank_non_positive_amount():
    data = [
        {'Дата операции': '2025-06-10', 'Сумма операции': -100},
        {'Дата операции': '2025-06-10', 'Сумма операции': 0}
    ]
    assert investment_bank(data, '2025-06', limit=50) == 0.0
