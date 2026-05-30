import os
import requests
from typing import Dict, Any


def convert_currency(transaction: Dict[str, Any]) -> float:
    """
    Принимает словарь транзакции.
    Возвращает сумму в рублях (float).
    Если валюта RUB – возвращает amount как есть.
    Если валюта USD или EUR – запрашивает курс через API и конвертирует.
    При ошибке API или отсутствии ключа возвращает 0.0.
    """
    amount_str = transaction.get("operationAmount", {}).get("amount")
    currency_code = transaction.get("operationAmount", {}).get("currency", {}).get("code")

    if amount_str is None or currency_code is None:
        return 0.0

    try:
        amount = float(amount_str)
    except ValueError:
        return 0.0

    if currency_code == "RUB":
        return amount

    if currency_code not in ("USD", "EUR"):
        # По заданию конвертируем только USD и EUR, остальные можно пропустить
        return 0.0

    # Получаем API-ключ из переменных окружения
    api_key = os.getenv("EXCHANGE_RATES_API_KEY")
    if not api_key:
        return 0.0

    url = "https://api.apilayer.com/exchangerates_data/latest"
    headers = {"apikey": api_key}
    params = {"base": currency_code, "symbols": "RUB"}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        rate = data.get("rates", {}).get("RUB")
        if rate is None:
            return 0.0
        return amount * rate
    except (requests.RequestException, KeyError, ValueError):
        return 0.0
