# Personal Assistant

Персональний помічник у вигляді desktop/TUI-застосунку для зберігання контактів, нагадування про дні народження та ведення текстових нотаток.

Проєкт побудовано на [Textual](https://textual.textualize.io/) і працює в терміналі з керуванням клавіатурою та мишею.

## Можливості

### Контакти
- Додавання та видалення контактів.
- Зміна імені і декількох телефонів одного контакту.
- Зберігання email та поштової адреси.
- Пошук за ім'ям, телефоном або email.
- Валідація телефонів (рівно 10 цифр), email та адрес.

### Дні народження
- Додавання, редагування та видалення дня народження.
- Формат дати `ДД.MM.РРРР`.
- Пошук найближчих дат народження на заданий період від 1 до 365 днів.
- Перенесення привітання із вихідних на наступний понеділок.
- Коректна обробка 29 лютого в невисокосні роки.

### Нотатки
- Створення, перегляд, редагування та видалення нотаток.
- Текст нотатки обмежено 500 символами.
- Додавання та видалення тегів.
- Пошук за текстом, тегом або пов'язаним контактом.
- Групування нотаток за тегами.
- Прив'язка нотатки до контакту та перегляд усіх нотаток контакту.
- Підтвердження перед видаленням.

### Інтерфейс
- Чотири вкладки: Dashboard, Contacts, Birthdays і Notes.
- Підказки синтаксису.
- Рядок стану та інтерактивні таблиці даних.
- Автоматичне оновлення інформації після кожної команди.

## Вимоги

- Python 3.10 або новіше.
- Пакети: `textual`, `rich`, `colorama`.

## Встановлення

### Windows

```powershell
git clone https://github.com/Wghaaj/goit-py-final-project.git
cd goit-py-final-project

py -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### macOS / Linux

```bash
git clone https://github.com/Wghaaj/goit-py-final-project.git
cd goit-py-final-project

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Запуск

```bash
python main.py
```

Щоб вийти з застосунку, введіть команду `exit` або скористайтеся стандартним виходом термінала.

## Команди

Команди вводяться в нижній рядок застосунку. Вводити назви у потрібному регістрі не обов'язково: команда автоматично приводиться до нижнього регістру.

### Контакти

| Команда | Опис | Приклад |
|---|---|---|
| `hello` | вивести привітання | `hello` |
| `add [name] [phone]` | додати контакт або телефон до існуючого контакту | `add Ivan 1234567890` |
| `remove [name]` | видалити контакт | `remove Ivan` |
| `change-name [old name] [new name]` | змінити ім'я контакту | `change-name Ivan Ivan Petrenko` |
| `change [name] [old phone] [new phone]` | змінити номер телефону | `change Ivan 1234567890 0987654321` |
| `phone [name]` | показати телефони контакту | `phone Ivan` |
| `all` | показати всі контакти | `all` |
| `search [query]` | пошук за іменем, телефоном або email | `search Ivan` |
| `add-email [name] [email]` | додати email | `add-email Ivan ivan@example.com` |
| `change-email [name] [new email]` | змінити email | `change-email Ivan ivan.petrenko@example.com` |
| `remove-email [name]` | видалити email | `remove-email Ivan` |
| `add-address [name] [address]` | додати адресу | `add-address Ivan Kyiv, Khreshchatyk 1` |
| `change-address [name] [new address]` | змінити адресу | `change-address Ivan Kyiv, Shevchenka 10` |
| `remove-address [name]` | видалити адресу | `remove-address Ivan` |

### Дні народження

| Команда | Опис | Приклад |
|---|---|---|
| `add-birthday [name] [DD.MM.YYYY]` | додати день народження | `add-birthday Ivan 15.08.1995` |
| `change-birthday [name] [DD.MM.YYYY]` | змінити день народження | `change-birthday Ivan 16.08.1995` |
| `remove-birthday [name]` | видалити день народження | `remove-birthday Ivan` |
| `show-birthday [name]` | показати день народження | `show-birthday Ivan` |
| `birthdays [days]` | показати найближчі дні народження; за замовчуванням — 7 днів | `birthdays 30` |

### Нотатки

| Команда | Опис | Приклад |
|---|---|---|
| `add-note [text]` | додати нотатку | `add-note Купити подарунок` |
| `notes` | усі нотатки | `notes` |
| `show-note [id]` | нотатка з датами створення й зміни | `show-note 1` |
| `find-note [text]` | пошук у тексті, тегах і контакті | `find-note подарунок` |
| `edit-note [id] [text]` | змінити текст | `edit-note 1 Купити квіти` |
| `delete-note [id]` | видалити | `delete-note 1` |
| `add-tag [id] [tag ...]` | додати один чи кілька тегів | `add-tag 1 shopping birthday` |
| `remove-tag [id] [tag]` | прибрати тег | `remove-tag 1 shopping` |
| `find-tag [tag]` | нотатки з тегом | `find-tag shopping` |
| `sort-notes` | нотатки, згруповані за тегами за алфавітом | `sort-notes` |
| `link-note [id] [name]` | прив'язати нотатку до контакту | `link-note 1 Olena` |
| `unlink-note [id]` | прибрати прив'язку | `unlink-note 1` |
| `contact-notes [name]` | нотатки контакту | `contact-notes Olena` |

## Збереження даних

Контакти та нотатки зберігаються разом у файл `addressbook.pkl` у корені проєкту. Дані завантажуються під час запуску та автоматично зберігаються після виконання команди.

Під час видалення чи перейменування контакту не видаляються пов'язані нотатки:
- при видаленні прив'язка прибирається;
- при перейменуванні прив'язка оновлюється.

## Структура проєкту

```text
.
├── main.py                 Точка входу
├── ui.py                   Головний Textual-застосунок
├── commands.py             Список і синтаксис команд
├── command_handler.py      Маршрутизація команд
├── contact_commands.py     Обробники контактів і днів народження
├── note_commands.py        Обробники нотаток, тегів і зв'язків
├── models.py               Моделі контактів та адресної книги
├── notes.py                Моделі нотаток і notebook
├── storage.py              Збереження та завантаження даних
├── utils.py                Парсинг і обробка помилок
├── components/             Заголовок, поле команд і модальні вікна
├── views/                  Вкладки Dashboard, Contacts, Birthdays і Notes
├── styles/                 CSS/TCSS-стилі інтерфейсу
├── requirements.txt        Залежності Python
└── addressbook.pkl         Локальна база даних, створюється автоматично
```
