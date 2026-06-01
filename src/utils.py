"""
Модуль для чтения транзакций из JSON-файла.
Добавлено логирование (успешные и ошибочные случаи).
"""

import json
import logging
import os
from typing import Any, Dict, List

# Создаём папку logs в корне проекта, если её нет
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# Создаём логгер для модуля utils
logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)

# Создаём файловый handler (перезапись при каждом запуске)
file_handler = logging.FileHandler(os.path.join(log_dir, "utils.log"), mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# Настраиваем формат лога: время - имя логгера - уровень - сообщение
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Добавляем handler к логгеру
logger.addHandler(file_handler)


def get_transactions_from_json(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON-файл с транзакциями и возвращает список словарей.

    Если файл не найден, пустой или содержимое не является списком,
    возвращает пустой список.
    """
    logger.debug(f"Попытка чтения файла: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list):
            logger.info(f"Успешно загружено {len(data)} транзакций из {file_path}")
            return data
        else:
            logger.error(f"Файл {file_path} содержит не список, а {type(data).__name__}. Возвращаем пустой список.")
            return []
    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON в файле {file_path}: {e}")
        return []
    except OSError as e:
        logger.error(f"Ошибка ввода-вывода при чтении файла {file_path}: {e}")
        return []
