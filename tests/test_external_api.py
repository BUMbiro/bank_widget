"""
Тесты для модуля external_api (конвертация валют).
Используется unittest.mock для подмены requests.get и переменных окружения.
"""

from unittest.mock import patch
from src.external_api import convert_currency


def test_convert_currency_rub():
    """Транзакция в рублях – возвращаем сумму без запроса к API."""
    transaction = {
        "operationAmount": {
            "amount": "100.50",
            "currency": {"code": "RUB"}
        }
    }
    assert convert_currency(transaction) == 100.50


def test_convert_currency_usd_success():
    """Транзакция в USD – успешная конвертация через API."""
    transaction = {
        "operationAmount": {
            "amount": "10",
            "currency": {"code": "USD"}
        }
    }
    # Подменяем requests.get
    with patch("src.external_api.requests.get") as mock_get:
        # Настраиваем ответ API
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {"rates": {"RUB": 75.5}}

        # Подменяем переменную окружения
        with patch.dict("os.environ", {"EXCHANGE_RATES_API_KEY": "fake_key"}):
            result = convert_currency(transaction)

    assert result == 10 * 75.5


def test_convert_currency_eur_success():
    """Транзакция в EUR – успешная конвертация."""
    transaction = {
        "operationAmount": {
            "amount": "20",
            "currency": {"code": "EUR"}
        }
    }
    with patch("src.external_api.requests.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {"rates": {"RUB": 85.0}}

        with patch.dict("os.environ", {"EXCHANGE_RATES_API_KEY": "fake_key"}):
            result = convert_currency(transaction)

    assert result == 20 * 85.0


def test_convert_currency_missing_api_key():
    """Если ключ API отсутствует в окружении, возвращаем 0.0."""
    transaction = {
        "operationAmount": {
            "amount": "10",
            "currency": {"code": "USD"}
        }
    }
    # Очищаем переменные окружения
    with patch.dict("os.environ", {}, clear=True):
        result = convert_currency(transaction)
        assert result == 0.0


import requests

def test_convert_currency_api_request_fails():
    """Ошибка при запросе к API – возвращаем 0.0."""
    transaction = {
        "operationAmount": {
            "amount": "10",
            "currency": {"code": "USD"}
        }
    }
    with patch("src.external_api.requests.get") as mock_get:
        # Используем исключение из пакета requests, которое перехватывается нашим кодом
        mock_get.side_effect = requests.RequestException("Network error")
        with patch.dict("os.environ", {"EXCHANGE_RATES_API_KEY": "fake_key"}):
            result = convert_currency(transaction)
            assert result == 0.0


def test_convert_currency_api_returns_no_rate():
    """API вернул ответ, но курс RUB отсутствует."""
    transaction = {
        "operationAmount": {
            "amount": "10",
            "currency": {"code": "USD"}
        }
    }
    with patch("src.external_api.requests.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {"rates": {}}
        with patch.dict("os.environ", {"EXCHANGE_RATES_API_KEY": "fake_key"}):
            result = convert_currency(transaction)
            assert result == 0.0


def test_convert_currency_invalid_amount_string():
    """Сумма в транзакции не число – возвращаем 0.0."""
    transaction = {
        "operationAmount": {
            "amount": "abc",
            "currency": {"code": "USD"}
        }
    }
    with patch.dict("os.environ", {"EXCHANGE_RATES_API_KEY": "fake_key"}):
        result = convert_currency(transaction)
        assert result == 0.0


def test_convert_currency_unsupported_currency():
    """Если валюта не RUB, не USD и не EUR – возвращаем 0.0."""
    transaction = {
        "operationAmount": {
            "amount": "100",
            "currency": {"code": "GBP"}
        }
    }
    result = convert_currency(transaction)
    assert result == 0.0


def test_convert_currency_missing_amount_key():
    """В транзакции нет ключа operationAmount или amount."""
    transaction = {}
    result = convert_currency(transaction)
    assert result == 0.0

    transaction2 = {"operationAmount": {}}
    result2 = convert_currency(transaction2)
    assert result2 == 0.0


def test_convert_currency_missing_currency_code():
    """Отсутствует код валюты."""
    transaction = {
        "operationAmount": {
            "amount": "100",
            "currency": {}
        }
    }
    result = convert_currency(transaction)
    assert result == 0.0
