import json
import os
import time
import pytest
from dotenv import load_dotenv
from src.views import (
    get_greeting,
    get_cards_info,
    get_top_transactions,
    get_currency_rates,
    get_stock_prices,
    main_page
)


@pytest.fixture
def sample_transactions():
    return [
        {'Номер карты': '1234', 'Сумма операции': 1000, 'Дата операции': '2020-05-10'},
        {'Номер карты': '5678', 'Сумма операции': 2000, 'Дата операции': '2020-05-15'},
        {'Номер карты': '1234', 'Сумма операции': 500, 'Дата операции': '2020-05-20'},
        {'Номер карты': '5678', 'Сумма операции': -300, 'Дата операции': '2020-05-25'},
        {'Номер карты': '9012', 'Сумма операции': 3000, 'Дата операции': '2020-05-01'},
    ]


def test_get_greeting():
    greeting = get_greeting()
    assert isinstance(greeting, str)
    assert greeting in ('Доброе утро', 'Добрый день', 'Добрый вечер', 'Доброй ночи')


def test_get_cards_info(sample_transactions):
    result = get_cards_info(sample_transactions)
    expected = [
        {'last_digits': '1234', 'total_spent': 1500.0, 'cashback': 15.0},
        {'last_digits': '5678', 'total_spent': 2000.0, 'cashback': 20.0},
        {'last_digits': '9012', 'total_spent': 3000.0, 'cashback': 30.0},
    ]
    assert len(result) == 3
    for item in expected:
        assert item in result


def test_get_top_transactions(sample_transactions):
    top = get_top_transactions(sample_transactions, n=3)
    assert len(top) == 3
    sorted_tx = sorted(sample_transactions, key=lambda x: abs(x['Сумма операции']), reverse=True)
    assert top[0]['amount'] == sorted_tx[0]['Сумма операции']
    assert top[1]['amount'] == sorted_tx[1]['Сумма операции']
    assert top[2]['amount'] == sorted_tx[2]['Сумма операции']


def test_get_currency_rates():
    currencies = ['USD', 'EUR']
    result = get_currency_rates(currencies)
    assert len(result) == 2
    for r in result:
        assert 'currency' in r
        assert 'rate' in r
        assert isinstance(r['rate'], float)


def test_get_stock_prices():
    load_dotenv()
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    if not api_key:
        pytest.skip("ALPHA_VANTAGE_API_KEY не задан, пропускаем тест")

    stocks = ['AAPL', 'AMZN', 'GOOGL']
    result = []
    max_retries = 3
    for stock in stocks:
        for attempt in range(max_retries):
            data = get_stock_prices([stock])
            if data and data[0].get('price', 0) > 0:
                result.extend(data)
                break
            else:
                time.sleep(2)  # ждём 2 секунды перед повторной попыткой
        else:
            pytest.skip(f"Не удалось получить цену для {stock} после {max_retries} попыток (возможно, лимит API)")

    assert len(result) == 3
    for r in result:
        assert 'stock' in r
        assert 'price' in r
        assert r['price'] > 0


def test_main_page(sample_transactions, monkeypatch):
    settings = {"user_currencies": ["USD"], "user_stocks": ["AAPL"]}

    def mock_open(*_args, **_kwargs):
        class MockFile:
            @staticmethod
            def read():
                return json.dumps(settings)

            def __enter__(self):
                return self

            def __exit__(self, *__args):
                pass

        return MockFile()

    monkeypatch.setattr("builtins.open", mock_open)

    result = main_page("2020-05-20", sample_transactions)
    assert "greeting" in result
    assert "cards" in result
    assert "top_transactions" in result
    assert "currency_rates" in result
    assert "stock_prices" in result
    assert result["currency_rates"][0]["currency"] == "USD"
    assert result["stock_prices"][0]["stock"] == "AAPL"
