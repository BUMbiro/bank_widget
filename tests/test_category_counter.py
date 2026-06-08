from src.category_counter import count_operations_by_categories


def test_count_operations():
    data = [{"description": "перевод"}, {"description": "перевод"}, {"description": "оплата"}]
    categories = ["перевод", "оплата", "налог"]
    result = count_operations_by_categories(data, categories)
    assert result == {"перевод": 2, "оплата": 1, "налог": 0}
