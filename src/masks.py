"""
Модуль маскировки банковских карт и счетов.
Добавлено логирование (успешные и ошибочные случаи).
"""

import logging
import os

# Создаём папку logs в корне проекта, если её нет
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# Создаём логгер для модуля masks
logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)  # Уровень DEBUG и выше

# Создаём файловый handler (перезапись при каждом запуске)
file_handler = logging.FileHandler(os.path.join(log_dir, "masks.log"), mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# Настраиваем формат лога: время - имя логгера - уровень - сообщение
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Добавляем handler к логгеру
logger.addHandler(file_handler)


def get_mask_card_number(card_number: int) -> str:
    """
    Принимает номер карты (int) и возвращает маску в формате XXXX XX** **** XXXX.

    Пример: 7000792289606361 -> '7000 79** **** 6361'
    """
    logger.debug(f"Вызов get_mask_card_number с card_number={card_number}")
    try:
        card_str = str(card_number)
        first_block = card_str[:4]
        second_block = card_str[4:6]
        last_block = card_str[-4:]
        result = f"{first_block} {second_block}** **** {last_block}"
        logger.info(f"Успешная маскировка карты: {card_number} -> {result}")
        return result
    except Exception as e:
        logger.error(f"Ошибка при маскировке карты {card_number}: {e}", exc_info=True)
        raise  # повторно выбрасываем исключение, чтобы не менять поведение


def get_mask_account(account_number: int) -> str:
    """
    Принимает номер счёта (int) и возвращает маску в формате **XXXX.

    Пример: 73654108430135874305 -> '**4305'
    """
    logger.debug(f"Вызов get_mask_account с account_number={account_number}")
    try:
        acc_str = str(account_number)
        result = f"**{acc_str[-4:]}"
        logger.info(f"Успешная маскировка счёта: {account_number} -> {result}")
        return result
    except Exception as e:
        logger.error(f"Ошибка при маскировке счёта {account_number}: {e}", exc_info=True)
        raise
