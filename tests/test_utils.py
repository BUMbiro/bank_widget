import pandas as pd

from src.utils import filter_transactions_by_date_range, read_transactions_from_excel


def test_filter_transactions_by_date_range():
    data = [
        {"Дата операции": "2020-05-01", "id": 1},
        {"Дата операции": "2020-05-15", "id": 2},
        {"Дата операции": "2020-05-31", "id": 3},
        {"Дата операции": "2020-06-01", "id": 4},
        {"Дата операции": "01.06.2020", "id": 5},
    ]
    filtered = filter_transactions_by_date_range(data, "2020-05-20")
    assert len(filtered) == 2
    assert filtered[0]["id"] == 1
    assert filtered[1]["id"] == 2


def test_filter_transactions_by_date_range_empty():
    assert filter_transactions_by_date_range([], "2020-05-20") == []


def test_filter_transactions_by_date_range_invalid_date():
    data = [{"Дата операции": "не дата", "id": 1}]
    filtered = filter_transactions_by_date_range(data, "2020-05-20")
    assert filtered == []


def test_filter_transactions_by_date_range_no_date_key():
    data = [{"id": 1}]
    filtered = filter_transactions_by_date_range(data, "2020-05-20")
    assert filtered == []


def test_read_transactions_from_excel_success(tmp_path):
    df = pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"]})
    file_path = tmp_path / "test.xlsx"
    df.to_excel(file_path, index=False)
    result = read_transactions_from_excel(str(file_path))
    assert len(result) == 2
    assert result[0]["col1"] == 1


def test_read_transactions_from_excel_error():
    result = read_transactions_from_excel("non_existent.xlsx")
    assert result == []


def test_read_transactions_from_excel_empty_file(tmp_path):
    empty_file = tmp_path / "empty.xlsx"
    pd.DataFrame().to_excel(empty_file, index=False)
    result = read_transactions_from_excel(str(empty_file))
    assert isinstance(result, list)


def test_read_transactions_from_excel_with_nan(tmp_path):
    df = pd.DataFrame({"A": [1, None, 3], "B": ["x", None, "z"]})
    file_path = tmp_path / "with_nan.xlsx"
    df.to_excel(file_path, index=False)
    result = read_transactions_from_excel(str(file_path))
    assert len(result) == 3
    assert result[1]["A"] is None
