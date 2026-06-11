from src.reports import spending_by_category, report_to_file
import json
import os
from datetime import datetime


def test_spending_by_category():
    data = [
        {'Дата операции': '2023-01-15', 'Сумма операции': 100, 'Категория': 'Еда'},
        {'Дата операции': '2023-02-10', 'Сумма операции': 200, 'Категория': 'Еда'},
        {'Дата операции': '2023-03-20', 'Сумма операции': 300, 'Категория': 'Еда'},
        {'Дата операции': '2023-04-01', 'Сумма операции': 400, 'Категория': 'Транспорт'},
    ]
    result = spending_by_category(data, 'Еда', '2023-03-31')
    assert len(result) == 3
    assert all(tx['Категория'] == 'Еда' for tx in result)


def test_spending_by_category_no_date():
    data = [{'Дата операции': datetime.now().strftime('%Y-%m-%d'), 'Сумма операции': 100, 'Категория': 'Еда'}]
    result = spending_by_category(data, 'Еда')
    assert len(result) == 1


def test_report_to_file_decorator():
    @report_to_file(filename='test_report.json')
    def dummy():
        return {'test': 123}

    dummy()
    assert os.path.exists('test_report.json')
    with open('test_report.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    assert data == {'test': 123}
    os.remove('test_report.json')


def test_report_to_file_default_name():
    @report_to_file()
    def dummy_default():
        return {'default': 456}

    dummy_default()
    files = [f for f in os.listdir('.') if f.startswith('dummy_default_') and f.endswith('.json')]
    assert len(files) == 1
    os.remove(files[0])
