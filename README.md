# QABuddy v0.1

QABuddy — Telegram-бот, который помогает готовиться к собеседованиям на позицию QA Engineer.

## ⚙️ Функции

- Команда `/start` — приветствие
- Команда `/question` — присылает случайный вопрос с ответом

## 📁 Структура проекта

- `bot.py` — основной файл бота
- `questions.json` — база знаний (вопросы и ответы)
- `config.py` — загрузка токена из `.env` (не хранит сам токен)
- `.env` — файл с реальным токеном (не коммитится в репозиторий)
- `.env.example` — пример файла с токеном (можно коммитить)
- `logs/bot.log` — файл логирования работы бота
- `requirements.txt` — список зависимостей проекта
- `.gitignore` — список исключений для Git

## 🔒 Безопасность токена

Токен Telegram-бота **не хранится в коде** и не попадает в репозиторий.  
Для этого используется файл `.env`, который добавлен в `.gitignore`.

### Как это работает
1. **Реальный токен** хранится в `.env`:
   ```env
   BOT_TOKEN=123456:ABCDEF_your_real_token_here
2. В файле config.py токен загружается с помощью python-dotenv:
    ```python
   from dotenv import load_dotenv
    import os

    load_dotenv()
    BOT_TOKEN = os.getenv("BOT_TOKEN")
3. Пример .env (.env.example) хранится в репозитории, чтобы показать формат:
    ```env
   BOT_TOKEN=PUT_YOUR_BOT_TOKEN_HERE
4. Файл .env указан в .gitignore и никогда не коммитится в GitHub.

## 🚀 Настройка

1. Скопируйте `.env.example` в `.env`:
   ```bash
   cp .env.example .env
2. В .env вставьте ваш токен от Telegram Bot API:
    ```env
    BOT_TOKEN=123456:ABCDEF_your_real_token_here
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
4. Запустите бота:
    ```bash
   python bot.py
