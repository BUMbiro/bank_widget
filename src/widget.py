# Импортируем функции маскировки из соседнего модуля masks
from src.masks import get_mask_account, get_mask_card_number

def mask_account_card(info: str) -> str:
    """
    Принимает строку с информацией о карте или счёте и возвращает её с замаскированным номером.

    Примеры:
        mask_account_card("Visa Platinum 7000792289606361")
        -> "Visa Platinum 7000 79** **** 6361"

        mask_account_card("Счет 73654108430135874305")
        -> "Счет **4305"
    """
    # Разделяем строку на две части по последнему пробелу
    # Например, "Visa Platinum 7000792289606361" -> ("Visa Platinum", "7000792289606361")
    parts = info.rsplit(' ', 1)

    # Если получилось не две части (нет пробела или пустая строка), возвращаем как есть
    if len(parts) != 2:
        return info

    # Первая часть — название (тип карты или счёт), вторая — номер
    name, number = parts

    # Проверяем, является ли тип "Счет" (без учёта регистра, на случай "счет" или "Счёт")
    if name.lower().startswith('счет'):
        # Для счёта используем get_mask_account, номер приводим к целому числу
        masked_number = get_mask_account(int(number))
    else:
        # Для карты используем get_mask_card_number
        masked_number = get_mask_card_number(int(number))

    # Склеиваем название и замаскированный номер
    return f"{name} {masked_number}"


def get_date(date_string: str) -> str:
    """
    Принимает строку с датой в формате ISO (например, "2024-03-11T02:26:18.671407")
    и возвращает дату в формате ДД.ММ.ГГГГ (например, "11.03.2024").
    """
    # Берём часть до буквы T (там находится дата в формате ГГГГ-ММ-ДД)
    date_part = date_string.split('T')[0]

    # Разделяем строку по дефисам на год, месяц, день
    year, month, day = date_part.split('-')

    # Возвращаем в порядке день, месяц, год, разделённые точками
    return f"{day}.{month}.{year}"