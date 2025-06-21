# Lifebot — Telegram Bot for Site Monitoring

[![python](https://img.shields.io/badge/Python-3.13-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![Poetry Version](https://img.shields.io/badge/poetry-2.1.3-blue?logo=python&style=flat-square)](https://python-poetry.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
![Docker Image Size](https://img.shields.io/badge/docker-image_~400MB-blue?style=flat-square&logo=docker)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue?logo=postgresql&style=flat-square)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7.2_alpine-red?logo=redis&style=flat-square)](https://redis.io/)

---

## Описание

BlumenHorizon Lifebot — это Telegram-бот для мониторинга статусов сайтов.  
Код хорошо декомпозирован, покрыт строгой проверкой типов (mypy), и работает с PostgreSQL и Redis для постоянных и временных данных соответственно.

---

## Технологии и стек

- Python с управлением зависимостями через [Poetry 2.1.3](https://python-poetry.org/)
- Полное покрытие типов с [mypy strict mode](https://mypy-lang.org/)
- Docker Compose с конфигурацией для разработки (`docker-compose.dev.yml`)
- PostgreSQL 17 для хранения постоянных данных
- Redis 7.2-alpine для временных данных (особенно для периодических заданий бота)
- Легковесный `Justfile` для автоматизации задач
- Логирование с помощью [Loguru](https://github.com/Delgan/loguru) с сохранением логов в файл `src/logs/bot.log`
- Форматирование кода: `black`, `isort`, `autoflake`

---

## Размеры и качество

- Контейнер основного приложения весит около **266 МБ**
- Код протестирован вручную на работу с сайтами
- Код хорошо декомпозирован, но есть пространство для улучшений

---

## Запуск и настройка

1. Получите токен вашего Telegram-бота через [BotFather](https://t.me/BotFather)
2. Отправьте первое сообщение боту, чтобы он активировался
3. Получите `user_id` и `chat_id` для администратора — вы можете получить их через [@userinfobot](https://t.me/userinfobot)
4. В `.env` или `.env.dev` заполните следующие переменные:
   - `BOT_TOKEN` — токен бота из BotFather
   - `TELEGRAM_ADMINS` — список ID администраторов, разделённых `;` (например, `123456;789012`)
   - `ALLOWED_CHAT_IDS` — список разрешённых ID чатов, разделённых `;`
   - `DB_URL` — строка подключения к PostgreSQL, например `postgresql+asyncpg://user:pass@postgres:5432/dbname`
   - `REDIS_URL` — URL подключения к Redis, например `redis://redis:6379`

5. Запустите бота командой:
   ```bash
   docker compose -f docker-compose.dev.yml up
