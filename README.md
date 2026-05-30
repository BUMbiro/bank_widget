# 🏦 Bank Widget

**Виджет для безопасного отображения банковских операций**

Привет! Это небольшой Python-проект, который поможет тебе:

- 🃏 **Маскировать** номера карт и счетов
- 📅 **Превращать** технические даты в человеческий формат `ДД.ММ.ГГГГ`
- 🔍 **Фильтровать** операции по статусу (`EXECUTED`, `CANCELED`, `PENDING`)
- 📆 **Сортировать** историю по дате (от новых к старым или наоборот)
- 📦 **Обрабатывать транзакции с помощью генераторов** (экономия памяти)
- 🧩 **Логировать** выполнение функций через декоратор `log`
- 📂 **Загружать** транзакции из JSON-файла
- 💱 **Конвертировать** валюту (USD/EUR → RUB) через внешнее API

Проект написан в учебных целях, но код полностью рабочий и может использоваться в реальных банковских приложениях.

---

## ✨ Особенности

- **Маскировка карт** – `Visa Platinum 7000 79** **** 6361`
- **Маскировка счетов** – `**4305`
- **Фильтр по статусу** – оставить только выполненные операции
- **Сортировка по дате** – одним вызовом функции
- **Тесты** – покрытие кода тестами **98%**
- **Готово к использованию** – просто установи и импортируй нужные функции

---

## 🚀 Быстрый старт
- Клонируй репозиторий

```bash
git clone https://github.com/BUMbiro/bank_widget.git
cd bank_widget
```

- Установи Poetry (если ещё нет)

```bash
pip install poetry
```
- Установи зависимости

```bash
poetry install
```
Проект использует только стандартные библиотеки Python + инструменты разработки (pytest, flake8, black, isort, mypy).

- Активируй окружение (опционально)

```bash
poetry shell
```

## 💡 Как этим пользоваться? (живые примеры)

## 🃏 Маскировка карты или счёта

```python
from src.widget import mask_account_card

print(mask_account_card("Visa Platinum 7000792289606361"))
# Visa Platinum 7000 79** **** 6361

print(mask_account_card("Счет 73654108430135874305"))
# Счет **4305

print(mask_account_card("Некорректная строка"))
# Некорректная строка (без ошибки)
```

## 📅 Преобразование даты в удобный формат

```python
from src.widget import get_date

print(get_date("2024-03-11T02:26:18.671407"))  # 11.03.2024
print(get_date("2025-12-31T23:59:59"))         # 31.12.2025
```

## 🔍 Фильтрация операций по статусу

```python
from src.processing import filter_by_state

operations = [
    {"id": 1, "state": "EXECUTED", "date": "2023-01-01"},
    {"id": 2, "state": "CANCELED", "date": "2023-01-02"},
    {"id": 3, "state": "EXECUTED", "date": "2023-01-03"}
]

executed = filter_by_state(operations)   # по умолчанию 'EXECUTED'
print(f"Успешных операций: {len(executed)}")   # 2

canceled = filter_by_state(operations, "CANCELED")
print(f"Отменённых операций: {len(canceled)}") # 1
```

## 📆 Сортировка операций по дате

```python
from src.processing import sort_by_date

ops = [
    {"id": 1, "date": "2024-01-01T10:00:00"},
    {"id": 2, "date": "2024-03-15T12:30:00"},
    {"id": 3, "date": "2024-02-20T18:00:00"}
]

sorted_newest = sort_by_date(ops)                # по убыванию (новые сверху)
print([op["id"] for op in sorted_newest])        # [2, 3, 1]

sorted_oldest = sort_by_date(ops, descending=False)  # по возрастанию
print([op["id"] for op in sorted_oldest])        # [1, 3, 2]
```
---

## 📦 Генераторы для работы с транзакциями
В реальной жизни аналитикам часто приходится перебирать тысячи транзакций. Хранить всё сразу в памяти — накладно. Генераторы приходят на помощь: они выдают данные по одному, экономя ресурсы. В модуле src.generators мы сделали три удобных генератора.

🔍 filter_by_currency – фильтр по валюте

Хотите посмотреть только долларовые переводы? Пожалуйста!

```python
from src.generators import filter_by_currency

transactions = [
    {"id": 1, "operationAmount": {"currency": {"code": "USD"}}, "description": "Перевод организации"},
    {"id": 2, "operationAmount": {"currency": {"code": "USD"}}, "description": "Перевод со счета на счет"},
    {"id": 3, "operationAmount": {"currency": {"code": "RUB"}}, "description": "Перевод с карты на карту"},
]

usd_transactions = filter_by_currency(transactions, "USD")
print(next(usd_transactions)["description"])  # Перевод организации
print(next(usd_transactions)["description"])  # Перевод со счета на счет
```

📝 transaction_descriptions – только описания

Если нужно быстро пробежаться по описаниям операций (например, для поиска ключевых слов), этот генератор сделает всё за вас.

```python
from src.generators import transaction_descriptions

transactions = [
    {"id": 1, "description": "Перевод организации"},
    {"id": 2, "description": "Перевод со счета на счет"},
    {"id": 3, "description": "Перевод с карты на карту"},
]

descriptions = transaction_descriptions(transactions)
print(next(descriptions))
print(next(descriptions))
print(next(descriptions))
```

💳 card_number_generator – номера карт в диапазоне

Пригодится для тестирования или симуляции данных. Генератор выдаёт номера карт в формате XXXX XXXX XXXX XXXX от start до stop включительно.

```python
from src.generators import card_number_generator

for card in card_number_generator(1, 3):
    print(card)
# 0000 0000 0000 0001
# 0000 0000 0000 0002
# 0000 0000 0000 0003
```

Можно генерировать и большие диапазоны, хоть до 9999 9999 9999 9999.

---
Все эти функции покрыты тестами (pytest), используют фикстуры и параметризацию. Код лежит в src/generators.py, а тесты – в tests/test_generators.py. Если хочешь добавить свои валюты или расширить функциональность – смело форкай!

---

## 🧩 Декоратор `log` – логируй всё, что происходит

Когда программа работает «в тишине», сложно понять, что именно пошло не так. Чтобы не гадать, мы сделали удобный декоратор `log`. Он оборачивает любую функцию и записывает в лог:

- ✅ **Успех** – `название_функции ok`
- ❌ **Ошибку** – `название_функции error: тип_ошибки. Inputs: (аргументы), {ключевые аргументы}`

Логи можно отправлять **в консоль** (для отладки) или **в файл** (для архива).

---

# 🎯 Как пользоваться

```python
from src.decorators import log
```
###  Логи в консоль (для быстрой проверки)
```python
from src.decorators import log

@log()
def add(a, b):
    return a + b

add(3, 5)   # в консоли появится "add ok"
```
###  Логи в файл (для долгого хранения)
```python
from src.decorators import log

@log(filename="mylog.txt")
def divide(a, b):
    return a / b

divide(10, 2)   # в mylog.txt запишется "divide ok"
divide(10, 0)   # в mylog.txt запишется "divide error: ZeroDivisionError. Inputs: (10, 0), {}
```

---

### 💡 Зачем это нужно?
Отладка – видишь все вызовы функций без кучи print().

Мониторинг – можно отследить, где программа падает.

Аудит – сохраняешь историю вызовов в файл.

---
# 📂 Чтение транзакций из JSON-файла

В проекте появилась возможность загружать банковские операции из JSON-файла. Это удобно, когда данные уже лежат в структурированном виде. Функция `get_transactions_from_json` из модуля `utils` делает это за вас.

```python
from src.utils import get_transactions_from_json

transactions = get_transactions_from_json("data/operations.json")
print(f"Загружено {len(transactions)} транзакций")
```
Если файл не найден, пустой или содержит не список — функция вернёт [], чтобы код не падал.

---
# 💱 Конвертация валюты (USD / EUR → RUB)
В реальной жизни транзакции приходят в разных валютах. Функция convert_currency из модуля external_api автоматически пересчитывает сумму в рубли по текущему курсу.

```python
from src.external_api import convert_currency

tx_usd = {
    "operationAmount": {
        "amount": "100",
        "currency": {"code": "USD"}
    }
}

rub_amount = convert_currency(tx_usd)
print(f"Сумма в рублях: {rub_amount}")
```
Курс запрашивается через Exchange Rates Data API (требуется ключ). Для работы нужно добавить файл .env с переменной:

```text
EXCHANGE_RATES_API_KEY=твой_ключ_от_apilayer
```
Пример такого файла лежит в .env.example. Не забудь добавить .env в .gitignore, чтобы не засветить ключ.

---
# 🔍 Как это работает?
Если валюта RUB – возвращает сумму без изменений.

Если USD или EUR – делает запрос к API, получает курс и пересчитывает.

При любых ошибках (нет интернета, неверный ключ, недоступный сервер) возвращает 0.0, чтобы не ломать программу.

Для новых функций написаны тесты с использованием unittest.mock (подмена API-запросов и файловой системы). Все тесты проходят успешно!

---
## 🧪 Тестирование
Проект покрыт тестами на 100%. Для запуска тестов и проверки покрытия используй pytest.

Запуск всех тестов
```bash
poetry run pytest -v
```
Запуск с отчётом о покрытии (HTML)
```bash
poetry run pytest --cov=src --cov-report=html
```
После выполнения открой htmlcov/index.html в браузере, чтобы увидеть детальный отчёт.

Структура тестов

```bash
test_masks.py – маскировка карт и счетов
```
```bash
test_widget.py – функции mask_account_card и get_date
```
```bash
test_processing.py – фильтрация и сортировка
```
В тестах используются фикстуры и параметризация для проверки различных кейсов.

---

Тестирование генераторов (дополнение к разделу)
В разделе тестирования можно добавить, что:

Filter_by_currency проверена на валюты USD, RUB, EUR (последняя даёт пустой итератор).

Transaction_descriptions корректно отрабатывает даже на пустом списке.

Card_number_generator проверен на граничных значениях (0, 1, 9999999999999999) и на форматировании.

---

## 🛠️️ Для разработчиков (линтеры и форматтеры)
Если ты хочешь дорабатывать проект, вот полезные команды:

```bash
# Проверить стиль кода
poetry run flake8 src

# Проверить типы
poetry run mypy src

# Автоматически отформатировать код
poetry run black src

# Отсортировать импорты
poetry run isort src
```
Все эти инструменты уже настроены в проекте (.flake8, pyproject.toml).

---

---

## 📄 Лицензия
Проект распространяется под лицензией MIT. Делайте с ним что хотите, только автора упомяните 😊

---

## 🙌 Благодарности
Спасибо моему наставнику за ценные замечания и поддержку.
И спасибо тебе, пользователь, что заглянул в этот проект! Если найдёшь ошибку или захочешь предложить улучшение — создавай Issue или Pull Request на GitHub.

Удачи с банковскими виджетами! 💳🔥
