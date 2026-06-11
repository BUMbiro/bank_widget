# 🏦 Bank Widget

**Виджет для безопасного отображения банковских операций**

Привет! Это небольшой Python-проект, который поможет тебе:

- 🃏 **Маскировать** номера карт и счетов (чтобы не светить данные на экране)
- 📅 **Превращать** технические даты в человеческий формат `ДД.ММ.ГГГГ`
- 🔍 **Фильтровать** операции по статусу (`EXECUTED`, `CANCELED`, `PENDING`)
- 📆 **Сортировать** историю по дате (от новых к старым или наоборот)
- 📦 **Обрабатывать транзакции с помощью генераторов** (экономия памяти)
- 🧩 **Логировать** выполнение функций через декоратор `log`
- 📂 **Читать транзакции из CSV и Excel** (просто укажи путь к файлу)
- 🔍 **Искать** транзакции по описанию с помощью регулярных выражений
- 🧮 **Подсчитывать** количество операций по категориям
- 💻 **Интерактивный режим** – запуск `src.main`

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
Установи Poetry (если ещё нет)

```bash
pip install poetry
```
Установи зависимости

```bash
poetry install
```
Проект использует только стандартные библиотеки Python + инструменты разработки (pytest, flake8, black, isort, mypy).

Активируй окружение (опционально)

```bash
poetry shell
```
---
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
В реальной жизни аналитикам часто приходится перебирать тысячи транзакций. Хранить всё сразу в памяти — накладно.
Генераторы приходят на помощь: они выдают данные по одному, экономя ресурсы.
В модуле src.generators мы сделали три удобных генератора.

## 🔍 filter_by_currency – фильтр по валюте
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
## 📝 transaction_descriptions – только описания

Если нужно быстро пробежаться по описаниям операций (например, для поиска ключевых слов),
этот генератор сделает всё за вас.

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
## 💳 card_number_generator – номера карт в диапазоне

Пригодится для тестирования или симуляции данных.
Генератор выдаёт номера карт в формате XXXX XXXX XXXX XXXX от start до stop включительно.

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
## 🧩 Декоратор log – логируй всё, что происходит
Когда программа работает «в тишине», сложно понять, что именно пошло не так.
Чтобы не гадать, мы сделали удобный декоратор log. Он оборачивает любую функцию и записывает в лог:

✅ Успех – название_функции ok

❌ Ошибку – название_функции error: тип_ошибки. Inputs: (аргументы), {ключевые аргументы}

Логи можно отправлять в консоль (для отладки) или в файл (для архива).

## 🎯 Как пользоваться
```python
from src.decorators import log

# Логи в консоль (для быстрой проверки)
@log()
def add(a, b):
    return a + b

add(3, 5)   # в консоли появится "add ok"

# Логи в файл (для долгого хранения)
@log(filename="mylog.txt")
def divide(a, b):
    return a / b

divide(10, 2)   # в mylog.txt запишется "divide ok"
divide(10, 0)   # в mylog.txt запишется "divide error: ZeroDivisionError. Inputs: (10, 0), {}"
```
## 💡 Зачем это нужно?

Отладка – видишь все вызовы функций без кучи print().

Мониторинг – можно отследить, где программа падает.

Аудит – сохраняешь историю вызовов в файл.

---
## 📂 Загрузка транзакций из CSV и Excel
JSON – это хорошо, но в жизни данные часто приходят в CSV или Excel. Теперь и с ними можно работать.

```python
from src.file_io import read_transactions_from_csv, read_transactions_from_excel

# Открываем CSV
csv_transactions = read_transactions_from_csv("data/operations.csv")
print(f"Загружено {len(csv_transactions)} записей из CSV")

# Открываем Excel
excel_transactions = read_transactions_from_excel("data/operations.xlsx")
print(f"Из Excel: {len(excel_transactions)} операций")
```
Обе функции возвращают список словарей – точно так же, как и при чтении JSON.
Если файл не найден, пустой или битый, вернётся пустой список, и программа не упадёт.

Под капотом – библиотека pandas (она уже добавлена в проект, вместе с openpyxl для Excel).
Ничего дополнительно настраивать не нужно.

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

Структура тестов:

- test_masks.py – маскировка карт и счетов

- test_widget.py – функции mask_account_card и get_date

- test_processing.py – фильтрация и сортировка

В тестах используются фикстуры и параметризация для проверки различных кейсов.

---
## 🔍 Поиск транзакций по описанию
Функция search_transactions из модуля search_utils поможет найти все операции,
в описании которых встречается нужное слово (регистр не важен). Используется регулярное выражение.

```python
from src.search_utils import search_transactions

# Пример списка транзакций (обычно он загружается из файла)
sample_transactions = [
    {"description": "Перевод организации"},
    {"description": "Перевод со счета на счет"},
    {"description": "Оплата услуг"}
]

found = search_transactions(sample_transactions, "перевод")
print(f"Найдено {len(found)} переводов")  # Найдено 2
```

---
## 🧮 Подсчёт операций по категориям
Модуль category_counter считает, сколько раз каждая категория (например, «перевод», «оплата», «покупка»)
встречается в описаниях.

```python
from src.category_counter import count_operations_by_categories

sample_transactions = [
    {"description": "перевод"},
    {"description": "перевод"},
    {"description": "оплата"}
]

categories = ["перевод", "оплата", "покупка"]
stats = count_operations_by_categories(sample_transactions, categories)
print(stats)  # {'перевод': 2, 'оплата': 1, 'покупка': 0}
```

---
## 💻 Интерактивный режим
Запустите главный модуль:

```bash
poetry run python -m src.main
```
Программа предложит:

- выбрать источник данных (JSON, CSV, XLSX);

- отфильтровать операции по статусу (EXECUTED, CANCELED, PENDING);

- отсортировать по дате (по возрастанию/убыванию);

- оставить только рублёвые транзакции;

- найти операции по ключевому слову в описании.

Результат выводится в удобном табличном виде с маскировкой счетов и карт.

---
## 🎓 Курсовая работа: анализ банковских транзакций
Проект шагнул дальше: теперь он умеет работать с Excel‑файлом data/operations.xlsx, 
отдавать JSON для веб‑страниц, предлагать удобные сервисы 
(кешбэк, поиск по телефонам, инвесткопилку) и строить отчёты.

## 🖥️ Главная страница (views.py)
Принимает дату (например, 2020-05-20) и возвращает JSON:

- Приветствие по времени суток (Доброе утро / Добрый день / …)

- По каждой карте: последние 4 цифры, расходы за период, кешбэк (1% от трат)

- Топ‑5 транзакций по сумме

- Курсы валют (USD, EUR) и цены акций (AAPL, AMZN, …) – реальные из API (если есть ключи) или заглушки

```python
from src.utils import read_transactions_from_excel
from src.views import main_page

df = read_transactions_from_excel("data/operations.xlsx")
data = main_page("2020-05-20", df)
print(data["cards"])
```
## 🔧 Полезные сервисы (services.py)
## 📈 Выгодные категории кешбэка
За месяц считает, сколько кешбэка (1% от трат) можно получить по каждой категории.

```python
from src.services import profitable_cashback_categories
from src.utils import read_transactions_from_excel

transactions = read_transactions_from_excel("data/operations.xlsx")
cash = profitable_cashback_categories(transactions, 2025, 5)
print(cash)  # {'Супермаркеты': 123.45, ...}
```
## 📱 Поиск по телефонным номерам
Находит транзакции, в описании которых есть российский мобильный номер 
(в любом формате: +7 921 11-22-33, 89211112233 и т.д.).

```python
from src.services import search_by_phone_numbers
from src.utils import read_transactions_from_excel

transactions = read_transactions_from_excel("data/operations.xlsx")
found = search_by_phone_numbers(transactions)
print(f"Найдено {len(found)} операций с телефонами")
```
## 💰 Инвесткопилка
Округляет каждую покупку до заданного предела 
(10, 50 или 100 ₽) и возвращает, сколько удалось бы отложить за месяц.

```python
from src.services import investment_bank
from src.utils import read_transactions_from_excel

transactions = read_transactions_from_excel("data/operations.xlsx")
saved = investment_bank(transactions, "2025-06", limit=50)
print(f"Отложено в копилку: {saved} ₽")
```
## 📊 Отчёты (reports.py)
## 📆 Траты по категории за последние 3 месяца
Возвращает список транзакций выбранной категории за последние 
90 дней относительно указанной даты (или сегодня).

```python
from src.reports import spending_by_category
from src.utils import read_transactions_from_excel

transactions = read_transactions_from_excel("data/operations.xlsx")
report = spending_by_category(transactions, "Супермаркеты", "2025-06-10")
print(f"Найдено {len(report)} покупок")
```
## 💾 Декоратор report_to_file
Автоматически сохраняет результат отчёта в JSON-файл. 
Имя генерируется как имя_функции_дата_время.json или задаётся параметром.

```python
from src.reports import spending_by_category
from src.utils import read_transactions_from_excel

transactions = read_transactions_from_excel("data/operations.xlsx")
spending_by_category(transactions, "Кафе")   # создаст spending_by_category_20250611_143022.json
```
## 🧪 Тестирование
Все новые модули покрыты тестами (pytest, моки, фикстуры, параметризация).
80 тестов успешно проходят, покрытие ключевых модулей превышает 80%.

```bash
poetry run pytest -v --cov=src --cov-report=term
```
## 🔑 API-ключи (необязательно, но для реальных данных)
Если хотите получать актуальные курсы валют и цены акций, добавьте в корень проекта файл .env:

```text
EXCHANGE_RATE_API_KEY=ваш_ключ
ALPHA_VANTAGE_API_KEY=ваш_ключ
```
Ключи бесплатно получаются на exchangerate-api.com и alphavantage.co.

Всё это уже работает. Просто положите файл operations.xlsx в папку data, 
настройте ключи (по желанию) и запускайте.

---
## 🛠️ Для разработчиков (линтеры и форматтеры)
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
## 📄 Лицензия
Проект распространяется под лицензией MIT. Делайте с ним что хотите, только автора упомяните 😊

---
## 🙌 Благодарности
Спасибо моему наставнику за ценные замечания и поддержку.
И спасибо тебе, пользователь, что заглянул в этот проект!
Если найдёшь ошибку или захочешь предложить улучшение — создавай Issue или Pull Request на GitHub.

Удачи с банковскими виджетами! 💳🔥