from unittest.mock import MagicMock, patch

import pandas as pd

from src.file_io import read_transactions_from_csv, read_transactions_from_excel


def test_read_csv_success():
    """Успешное чтение CSV."""
    mock_df = MagicMock(spec=pd.DataFrame)
    mock_df.to_dict.return_value = [{"id": 1, "amount": 100}]
    with patch("pandas.read_csv", return_value=mock_df):
        result = read_transactions_from_csv("dummy.csv")
        assert result == [{"id": 1, "amount": 100}]


def test_read_csv_exception():
    """Ошибка при чтении CSV – возвращаем пустой список."""
    # Используем FileNotFoundError, который перехватывается кодом
    with patch("pandas.read_csv", side_effect=FileNotFoundError("File not found")):
        result = read_transactions_from_csv("missing.csv")
        assert result == []


def test_read_excel_success():
    """Успешное чтение Excel."""
    mock_df = MagicMock(spec=pd.DataFrame)
    mock_df.to_dict.return_value = [{"id": 2, "amount": 200}]
    with patch("pandas.read_excel", return_value=mock_df):
        result = read_transactions_from_excel("dummy.xlsx")
        assert result == [{"id": 2, "amount": 200}]


def test_read_excel_exception():
    """Ошибка при чтении Excel – возвращаем пустой список."""
    # Используем PermissionError, который перехватывается кодом
    with patch("pandas.read_excel", side_effect=PermissionError("File error")):
        result = read_transactions_from_excel("missing.xlsx")
        assert result == []
