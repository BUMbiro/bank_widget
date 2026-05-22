"""
Тесты для декоратора log.
"""

import pytest

from src.decorators import log


def test_log_to_console_success(capsys):
    """Логирование успешной функции в консоль."""

    @log()
    def add(a, b):
        return a + b

    add(3, 5)
    captured = capsys.readouterr()
    assert captured.out == "add ok\n"


def test_log_to_console_error(capsys):
    """Логирование функции с ошибкой в консоль."""

    @log()
    def add(a, b):
        return a + b

    # Сложение int и str вызывает TypeError
    with pytest.raises(TypeError):
        add(1, "2")

    captured = capsys.readouterr()
    assert captured.out == "add error: TypeError. Inputs: (1, '2'), {}\n"


def test_log_to_file_success(tmp_path):
    """Логирование успешной функции в файл."""
    log_file = tmp_path / "test.log"

    @log(filename=str(log_file))
    def multiply(a, b):
        return a * b

    multiply(2, 3)
    with open(log_file, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == "multiply ok\n"


def test_log_to_file_error(tmp_path):
    """Логирование ошибки в файл."""
    log_file = tmp_path / "test.log"

    @log(filename=str(log_file))
    def add(a, b):
        return a + b

    # Сложение int и str вызывает TypeError
    with pytest.raises(TypeError):
        add(1, "2")

    with open(log_file, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == "add error: TypeError. Inputs: (1, '2'), {}\n"


def test_log_with_kwargs(capsys):
    """Проверка логирования с именованными аргументами."""

    @log()
    def greet(name, greeting="Hello"):
        return f"{greeting}, {name}!"

    greet("Alice", greeting="Hi")
    captured = capsys.readouterr()
    assert captured.out == "greet ok\n"


def test_log_decorator_multiple_calls(tmp_path):
    """Проверка нескольких вызовов подряд (логи дописываются в файл)."""
    log_file = tmp_path / "multi.log"

    @log(filename=str(log_file))
    def square(x):
        return x * x

    square(2)
    square(3)
    with open(log_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    assert lines[0] == "square ok\n"
    assert lines[1] == "square ok\n"
