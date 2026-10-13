# Booking System

Система онлайн-записи клиентов с Telegram-ботом и простой веб-панелью.

## Возможности
- Запись клиентов через Telegram-бота (выбор даты/времени)
- Уведомления администратору о новых записях
- Простая веб-страница со списком записей
- Хранение в SQLite

## Стек
- Python 3.11+
- aiogram 3.x (бот)
- FastAPI + Jinja2 (веб-панель)
- SQLite

## Установка

```bash
git clone https://github.com/gdenikita/booking-system.git
cd booking-system
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Создай `.env`:
```
BOT_TOKEN=токен_от_BotFather
ADMIN_ID=твой_telegram_id
```

Запуск бота:
```bash
python bot.py
```

Запуск веб-панели (в другом терминале):
```bash
uvicorn web:app --reload --port 8000
```

Открой http://localhost:8000

## Структура
- `bot.py` — Telegram-бот
- `web.py` — веб-панель
- `database.py` — БД
- `keyboards.py` — клавиатуры бота
