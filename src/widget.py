"""Модуль для обработки информации о картах и счетах, а также дат."""

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(card_or_account_info: str) -> str:
    """
    Принимает строку с информацией о карте или счёте и возвращает её с маскированным номером.

    Формат входной строки: "<тип> <номер>".
    Для карт маскирует номер по правилу XXXX XX** **** XXXX,
    для счетов — **XXXX.

    Args:
        card_or_account_info (str): строка, содержащая тип и номер (например, 'Visa Platinum 7000792289606361').

    Returns:
        str: строка с замаскированным номером.

    Example:
        >>> mask_account_card('Visa Platinum 7000792289606361')
        'Visa Platinum 7000 79** **** 6361'
        >>> mask_account_card('Счет 73654108430135874305')
        'Счет **4305'
    """
    # Разделяем строку на части. Последняя часть — это номер, остальные — тип (могут содержать пробелы).
    parts = card_or_account_info.rsplit(' ', 1)
    if len(parts) != 2:
        # Если нет явного разделения на тип и номер, возвращаем как есть (или можно выбросить исключение, но по заданию так)
        return card_or_account_info

    card_type = parts[0]
    number_str = parts[1]

    # Если номер состоит только из цифр и его длина типична для карты (16) или счета (20) — можно определить автоматически.
    # Но по заданию нужно отличать по наличию слова "Счет" в начале.
    if card_type.lower().startswith('счет'):
        masked_number = get_mask_account(int(number_str))
    else:
        masked_number = get_mask_card_number(int(number_str))

    return f"{card_type} {masked_number}"


def get_date(date_string: str) -> str:
    """
    Принимает строку с датой в формате ISO (например, '2024-03-11T02:26:18.671407')
    и возвращает дату в формате 'ДД.ММ.ГГГГ'.

    Args:
        date_string (str): дата в ISO-формате.

    Returns:
        str: дата в формате 'ДД.ММ.ГГГГ'.

    Example:
        >>> get_date('2024-03-11T02:26:18.671407')
        '11.03.2024'
    """
    # Извлекаем только часть даты (до T) и преобразуем
    date_part = date_string.split('T')[0]
    year, month, day = date_part.split('-')
    return f"{day}.{month}.{year}"