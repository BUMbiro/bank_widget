# Импортируем библиотеку pandas для работы с CSV и Excel файлами
import pandas as pd
# Импортируем типы для аннотаций: List, Dict, Any, Hashable
from typing import List, Dict, Any, Hashable


def read_transactions_from_csv(file_path: str) -> List[Dict[Hashable, Any]]:
    """
    Читает финансовые транзакции из CSV-файла и возвращает список словарей.

    Параметры:
        file_path (str): путь к CSV-файлу.

    Возвращает:
        List[Dict[Hashable, Any]]: список словарей, где каждый словарь — одна транзакция.
                                   Ключи словаря — названия столбцов (обычно строки).
                                   В случае ошибки возвращается пустой список.
    """
    try:
        # Пытаемся прочитать CSV-файл в DataFrame pandas
        df = pd.read_csv(file_path)
        # Преобразуем DataFrame в список словарей (каждая строка -> словарь)
        return df.to_dict(orient='records')
    # Перехватываем конкретные исключения, которые могут возникнуть при чтении:
    # - FileNotFoundError: файл не найден
    # - PermissionError: нет прав на чтение
    # - pd.errors.EmptyDataError: файл пуст
    # - ValueError: ошибка парсинга (неверный формат)
    # - OSError: другие проблемы ввода-вывода
    except (FileNotFoundError, PermissionError, pd.errors.EmptyDataError, ValueError, OSError):
        # В случае любой ошибки возвращаем пустой список (согласно условию задания)
        return []


def read_transactions_from_excel(file_path: str) -> List[Dict[Hashable, Any]]:
    """
    Читает финансовые транзакции из Excel-файла (.xlsx) и возвращает список словарей.

    Параметры:
        file_path (str): путь к Excel-файлу.

    Возвращает:
        List[Dict[Hashable, Any]]: список словарей, где каждый словарь — одна транзакция.
                                   Ключи словаря — названия столбцов.
                                   При ошибке возвращается пустой список.
    """
    try:
        # Читаем Excel-файл (первый лист) в DataFrame pandas
        # Для работы требуется установленная библиотека openpyxl (уже добавлена в проект)
        df = pd.read_excel(file_path)
        # Преобразуем DataFrame в список словарей
        return df.to_dict(orient='records')
    # Перехватываем исключения, характерные для чтения Excel:
    # - FileNotFoundError: файл не найден
    # - PermissionError: нет прав на чтение
    # - ValueError: неверный формат (например, не .xlsx файл)
    # - OSError: другие ошибки ввода-вывода
    except (FileNotFoundError, PermissionError, ValueError, OSError):
        # Для Excel дополнительно может быть pd.errors.EmptyDataError,
        # но он наследуется от ValueError, поэтому перехватывается.
        # В любом случае возвращаем пустой список.
        return []