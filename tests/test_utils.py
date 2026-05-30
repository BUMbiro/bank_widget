"""
Тесты для модуля utils (чтение JSON-файла).
Используется встроенный unittest.mock для замены open и json.load.
"""

import json
from unittest.mock import patch, mock_open
from src.utils import get_transactions_from_json


def test_get_transactions_from_json_success():
    """Успешное чтение списка транзакций."""
    mock_data = [{"id": 1}, {"id": 2}]
    # Подменяем open: при вызове open возвращаем дескриптор, который читает json.dumps(mock_data)
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
        result = get_transactions_from_json("any_path.json")
        assert result == mock_data


def test_get_transactions_from_json_not_list():
    """Если в JSON не список (например, словарь), возвращаем пустой список."""
    mock_data = {"key": "value"}
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
        result = get_transactions_from_json("any_path.json")
        assert result == []


def test_get_transactions_from_json_file_not_found():
    """Файл не найден – возвращаем пустой список."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = get_transactions_from_json("missing.json")
        assert result == []


def test_get_transactions_from_json_invalid_json():
    """Некорректный JSON (ошибка парсинга) – возвращаем пустой список."""
    with patch("builtins.open", mock_open(read_data="not a json")):
        result = get_transactions_from_json("any_path.json")
        assert result == []


def test_get_transactions_from_json_os_error():
    """Любая другая ошибка ввода/вывода – возвращаем пустой список."""
    with patch("builtins.open", side_effect=OSError):
        result = get_transactions_from_json("any_path.json")
        assert result == []
