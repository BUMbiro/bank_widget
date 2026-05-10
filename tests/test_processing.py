import pytest
from src.processing import filter_by_state, sort_by_date

# ----- Фикстуры для данных -----
@pytest.fixture
def sample_data():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-01T10:00:00"},
        {"id": 2, "state": "CANCELED", "date": "2023-02-01T10:00:00"},
        {"id": 3, "state": "EXECUTED", "date": "2023-03-01T10:00:00"},
        {"id": 4, "state": "PENDING", "date": "2023-04-01T10:00:00"},
    ]

@pytest.fixture
def sample_data_same_dates():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-01T10:00:00"},
        {"id": 2, "state": "EXECUTED", "date": "2023-01-01T12:00:00"},
        {"id": 3, "state": "EXECUTED", "date": "2023-01-01T09:00:00"},
    ]

# ----- Тесты filter_by_state -----
def test_filter_by_state_default(sample_data):
    result = filter_by_state(sample_data)
    assert len(result) == 2
    assert all(item["state"] == "EXECUTED" for item in result)
    assert result[0]["id"] == 1
    assert result[1]["id"] == 3

def test_filter_by_state_canceled(sample_data):
    result = filter_by_state(sample_data, "CANCELED")
    assert len(result) == 1
    assert result[0]["state"] == "CANCELED"

def test_filter_by_state_no_match(sample_data):
    result = filter_by_state(sample_data, "NONEXISTENT")
    assert result == []

@pytest.mark.parametrize("state, expected_count", [
    ("EXECUTED", 2),
    ("CANCELED", 1),
    ("PENDING", 1),
    ("UNKNOWN", 0),
])
def test_filter_by_state_parametrized(sample_data, state, expected_count):
    result = filter_by_state(sample_data, state)
    assert len(result) == expected_count

# ----- Тесты sort_by_date -----
def test_sort_by_date_descending(sample_data):
    result = sort_by_date(sample_data)
    dates = [item["date"] for item in result]
    assert dates == ["2023-04-01T10:00:00", "2023-03-01T10:00:00", "2023-02-01T10:00:00", "2023-01-01T10:00:00"]

def test_sort_by_date_ascending(sample_data):
    result = sort_by_date(sample_data, descending=False)
    dates = [item["date"] for item in result]
    assert dates == ["2023-01-01T10:00:00", "2023-02-01T10:00:00", "2023-03-01T10:00:00", "2023-04-01T10:00:00"]

def test_sort_by_date_same_dates(sample_data_same_dates):
    result = sort_by_date(sample_data_same_dates, descending=True)
    # ожидаем стабильную сортировку: порядок по времени, но время из строки
    # сравниваем по id
    ids = [item["id"] for item in result]
    # в исходном списке: id=2 (12:00), id=1 (10:00), id=3 (09:00) - по убыванию: id2, id1, id3
    assert ids == [2, 1, 3]

def test_sort_by_date_empty_list():
    assert sort_by_date([]) == []
