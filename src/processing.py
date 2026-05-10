"""
Модуль для фильтрации и сортировки списков банковских операций.

Содержит функции:
- filter_by_state: фильтрация операций по статусу (state).
- sort_by_date: сортировка операций по дате (date).
"""

from typing import Any, Dict, List


def filter_by_state(operations: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Фильтрует список операций по заданному статусу.

    Функция возвращает новый список, содержащий только те словари,
    у которых значение ключа 'state' совпадает с переданным статусом.
    Если статус не указан, используется значение по умолчанию 'EXECUTED'.

    Аргументы:
        operations (List[Dict[str, Any]]): Список словарей с данными об операциях.
            Каждый словарь должен содержать ключ 'state'.
        state (str): Статус, по которому производится фильтрация.
            По умолчанию 'EXECUTED'.

    Возвращает:
        List[Dict[str, Any]]: Новый список, содержащий только операции с указанным статусом.

    Примеры:
        >>> data = [
        ...     {"id": 1, "state": "EXECUTED"},
        ...     {"id": 2, "state": "CANCELED"},
        ...     {"id": 3, "state": "EXECUTED"}
        ... ]
        >>> filter_by_state(data)
        [{'id': 1, 'state': 'EXECUTED'}, {'id': 3, 'state': 'EXECUTED'}]

        >>> filter_by_state(data, "CANCELED")
        [{'id': 2, 'state': 'CANCELED'}]

        >>> filter_by_state(data, "PENDING")
        []
    """
    return [item for item in operations if item.get("state") == state]


def sort_by_date(operations: List[Dict[str, Any]], descending: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует список операций по дате.

    Функция возвращает новый список, отсортированный по значению ключа 'date'.
    По умолчанию сортировка производится в порядке убывания (от новых к старым).
    Для сортировки в порядке возрастания (от старых к новым) передайте descending=False.

    Аргументы:
        operations (List[Dict[str, Any]]): Список словарей с данными об операциях.
            Каждый словарь должен содержать ключ 'date' со строкой в формате ISO
            (например, "2024-03-11T02:26:18.671407").
        descending (bool): Порядок сортировки. True – убывание (сначала новые),
            False – возрастание (сначала старые). По умолчанию True.

    Возвращает:
        List[Dict[str, Any]]: Новый отсортированный список.

    Примеры:
        >>> data = [
        ...     {"id": 1, "date": "2023-01-01T10:00:00"},
        ...     {"id": 2, "date": "2023-03-01T10:00:00"},
        ...     {"id": 3, "date": "2023-02-01T10:00:00"}
        ... ]
        >>> sort_by_date(data)
        [{'id': 2, 'date': '2023-03-01T10:00:00'}
        {'id': 3, 'date': '2023-02-01T10:00:00'}
        {'id': 1, 'date': '2023-01-01T10:00:00'}]

        >>> sort_by_date(data, descending=False)
        [{'id': 1, 'date': '2023-01-01T10:00:00'}
        {'id': 3, 'date': '2023-02-01T10:00:00'}
        {'id': 2, 'date': '2023-03-01T10:00:00'}]

        >>> sort_by_date([])
        []
    """
    return sorted(operations, key=lambda x: x.get("date", ""), reverse=descending)
