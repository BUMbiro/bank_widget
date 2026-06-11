"""
Модуль для генерации JSON-ответов для веб-страниц.
Использует реальные API для курсов валют и цен акций.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any

import requests
from dotenv import load_dotenv

from src.utils import read_transactions_from_excel, filter_transactions_by_date_range

# Загружаем переменные окружения из .env
load_dotenv()


def get_greeting() -> str:
    """Возвращает приветствие в зависимости от текущего времени."""
    hour = datetime.now().hour
    if 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_cards_info(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Возвращает информацию по каждой карте:
    последние 4 цифры, общая сумма расходов, кешбэк (1 рубль на каждые 100).
    """
    cards = {}
    for tx in transactions:
        card_num = tx.get('Номер карты')
        if not card_num:
            continue
        last_digits = str(card_num)[-4:]
        amount = tx.get('Сумма операции', 0)
        # Учитываем только расходы (положительные суммы)
        if amount > 0:
            spent = amount
            cashback = spent / 100
            if last_digits not in cards:
                cards[last_digits] = {'total_spent': 0, 'cashback': 0}
            cards[last_digits]['total_spent'] += spent
            cards[last_digits]['cashback'] += cashback
    result_list = []
    for last_digits, data in cards.items():
        result_list.append({
            'last_digits': last_digits,
            'total_spent': round(data['total_spent'], 2),
            'cashback': round(data['cashback'], 2)
        })
    return result_list


def get_top_transactions(transactions: List[Dict[str, Any]], n: int = 5) -> List[Dict[str, Any]]:
    """
    Возвращает топ-N транзакций по сумме платежа (по убыванию).
    """
    sorted_tx = sorted(transactions, key=lambda x: abs(x.get('Сумма операции', 0)), reverse=True)
    top = []
    for tx in sorted_tx[:n]:
        date_str = tx.get('Дата операции')
        if date_str:
            try:
                if isinstance(date_str, datetime):
                    date_obj = date_str
                else:
                    date_obj = datetime.strptime(str(date_str), '%Y-%m-%d')
                formatted_date = date_obj.strftime('%d.%m.%Y')
            except (ValueError, TypeError):
                formatted_date = str(date_str)
        else:
            formatted_date = ''
        amount = tx.get('Сумма операции', 0)
        category = tx.get('Категория', '')
        description = tx.get('Описание', '')
        top.append({
            'date': formatted_date,
            'amount': amount,
            'category': category,
            'description': description
        })
    return top


def get_currency_rates(currencies: List[str]) -> List[Dict[str, Any]]:
    api_key = os.getenv('EXCHANGE_RATE_API_KEY')
    rates = []
    for cur in currencies:
        rate = 0.0
        if api_key:
            url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{cur}"
            try:
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                data = response.json()
                rate = data.get('conversion_rates', {}).get('RUB', 0.0)
            except (requests.RequestException, KeyError, ValueError):
                pass
        rates.append({'currency': cur, 'rate': rate})
    return rates


def get_stock_prices(stocks: List[str]) -> List[Dict[str, Any]]:
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    prices = []
    for stock in stocks:
        price = 0.0
        if api_key:
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={api_key}"
            try:
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                data = response.json()
                price = float(data['Global Quote']['05. price'])
            except (requests.RequestException, KeyError, ValueError, TypeError):
                pass
        prices.append({'stock': stock, 'price': price})
    return prices


def main_page(date_str: str, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Главная страница: формирует JSON-ответ на основе транзакций за период
    с начала месяца по указанную дату.
    """
    filtered = filter_transactions_by_date_range(transactions, date_str)
    with open('user_settings.json', 'r', encoding='utf-8-sig') as f:
        settings = json.load(f)
    currencies = settings.get('user_currencies', [])
    stocks = settings.get('user_stocks', [])

    greeting = get_greeting()
    cards = get_cards_info(filtered)
    top = get_top_transactions(filtered, 5)
    currency_rates = get_currency_rates(currencies)
    stock_prices = get_stock_prices(stocks)

    return {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }


if __name__ == "__main__":
    # Пример для самопроверки
    df = read_transactions_from_excel("data/operations.xlsx")
    if df:
        result = main_page("2020-05-20", df)
        print(json.dumps(result, indent=2, ensure_ascii=False))
