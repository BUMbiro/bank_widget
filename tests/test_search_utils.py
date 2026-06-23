import pytest

from src.search_utils import search_transactions


@pytest.fixture
def sample():
    return [{"description": "Перевод организации"}, {"description": "Перевод со счета"}, {"description": "Оплата"}]


def test_search_found(sample):
    assert len(search_transactions(sample, "перевод")) == 2


def test_search_empty(sample):
    assert search_transactions(sample, "") == sample


def test_search_not_found(sample):
    assert search_transactions(sample, "покупка") == []
