"""Модуль маскировки банковских карт и счетов."""


def get_mask_card_number(card_number: int) -> str:
    """
    Принимает номер карты (int) и возвращает маску в формате XXXX XX** **** XXXX.

    Пример: 7000792289606361 -> '7000 79** **** 6361'
    """
    card_str = str(card_number)
    first_block = card_str[:4]
    second_block = card_str[4:6]
    last_block = card_str[-4:]
    return f"{first_block} {second_block}** **** {last_block}"


def get_mask_account(account_number: int) -> str:
    """
    Принимает номер счёта (int) и возвращает маску в формате **XXXX.

    Пример: 73654108430135874305 -> '**4305'
    """
    acc_str = str(account_number)
    return f"**{acc_str[-4:]}"
