from src.utils import filter_transactions_by_date_range, read_transactions_from_excel
import pandas as pd
import tempfile
import os


def test_filter_transactions_by_date_range():
    data = [
        {'Дата операции': '2020-05-01', 'id': 1},
        {'Дата операции': '2020-05-15', 'id': 2},
        {'Дата операции': '2020-05-31', 'id': 3},
        {'Дата операции': '2020-06-01', 'id': 4},
        {'Дата операции': '01.06.2020', 'id': 5},
    ]
    filtered = filter_transactions_by_date_range(data, '2020-05-20')
    assert len(filtered) == 2
    assert filtered[0]['id'] == 1
    assert filtered[1]['id'] == 2


def test_filter_transactions_by_date_range_empty():
    assert filter_transactions_by_date_range([], '2020-05-20') == []


def test_filter_transactions_by_date_range_invalid_date():
    data = [{'Дата операции': 'не дата', 'id': 1}]
    filtered = filter_transactions_by_date_range(data, '2020-05-20')
    assert filtered == []


def test_read_transactions_from_excel_success():
    df = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        df.to_excel(tmp.name, index=False)
        result = read_transactions_from_excel(tmp.name)
        assert len(result) == 2
        assert result[0]['col1'] == 1
    os.unlink(tmp.name)


def test_read_transactions_from_excel_error():
    result = read_transactions_from_excel('non_existent.xlsx')
    assert result == []


def test_read_transactions_from_excel_empty_file(tmp_path):
    """Проверка чтения пустого Excel-файла (должен вернуть пустой список)."""
    empty_file = tmp_path / "empty.xlsx"
    pd.DataFrame().to_excel(empty_file, index=False)
    result = read_transactions_from_excel(empty_file)
    assert result == []  # или список с одной пустой строкой? Уточни по поведению.


def test_filter_transactions_by_date_range_no_date_key():
    data = [{'id': 1}]  # нет ключа 'Дата операции'
    filtered = filter_transactions_by_date_range(data, '2020-05-20')
    assert filtered == []
