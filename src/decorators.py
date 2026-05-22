# type: ignore
"""
Модуль с декоратором логирования.
"""

import functools
from typing import IO, Any, Callable, Optional, Union  # noqa: F401


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования вызовов функций.

    При успешном выполнении записывает "function_name ok".
    При ошибке записывает "function_name error: ошибка. Inputs: args, kwargs".

    Если передан filename, логи пишутся в файл, иначе в консоль.

    Args:
        filename (Optional[str]): Имя файла для записи логов.

    Returns:
        Callable: Декоратор.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            log_message = ""  # <-- инициализация
            try:
                result = func(*args, **kwargs)
                log_message = f"{func.__name__} ok\n"
            except Exception as e:
                log_message = f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}\n"
                raise
            finally:
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(log_message)
                else:
                    print(log_message, end="")
            return result

        return wrapper

    return decorator
