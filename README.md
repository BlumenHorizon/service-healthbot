# Healthbot — Telegram Bot for Site Monitoring

[![python](https://img.shields.io/badge/Python-3.13-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![Poetry Version](https://img.shields.io/badge/poetry-2.1.3-blue?logo=python&style=flat-square)](https://python-poetry.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
![Docker Image Size](https://img.shields.io/badge/docker-image_~400MB-blue?style=flat-square&logo=docker)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue?logo=postgresql&style=flat-square)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7.2_alpine-red?logo=redis&style=flat-square)](https://redis.io/)

---

## Description

BlumenHorizon Healthbot is a Telegram bot for monitoring website statuses.  
The code is well decomposed, strictly typed (using mypy), and works with PostgreSQL and Redis for persistent and temporary data respectively.

---

## Technologies and Stack

- Python with dependency management via [Poetry 2.1.3](https://python-poetry.org/)
- Full type coverage with [mypy strict mode](https://mypy-lang.org/)
- Docker Compose configuration for development (`docker-compose.dev.yml`)
- PostgreSQL 17 for persistent data storage
- Redis 7.2-alpine for temporary data (especially for periodic bot tasks)
- Lightweight `Justfile` for task automation
- Logging with [Loguru](https://github.com/Delgan/loguru), saving logs to `src/logs/bot.log`
- Code formatting: `black`, `isort`, `autoflake`

---

## Size and Quality

- The main application container weighs about **266 MB**
- The code has been manually tested for website interactions
- The code is well structured, but there is room for improvements

---

## Running and Setup

1. Obtain your Telegram bot token via [BotFather](https://t.me/BotFather)
2. Send the first message to your bot to activate it
3. Get the `user_id` and `chat_id` for the administrator — you can get these via [@userinfobot](https://t.me/userinfobot)
4. Fill in the following variables in `.env` or `.env.dev`:
   - `BOT_TOKEN` — the token from BotFather
   - `TELEGRAM_ADMINS` — list of admin IDs separated by `;` (e.g., `123456;789012`)
   - `ALLOWED_CHAT_IDS` — list of allowed chat IDs separated by `;`
   - `DB_URL` — PostgreSQL connection string, for example `postgresql+asyncpg://user:pass@postgres:5432/dbname`
   - `REDIS_URL` — Redis connection URL, for example `redis://redis:6379`

5. Run the bot with the command:
   ```bash
   docker compose -f docker-compose.dev.yml up