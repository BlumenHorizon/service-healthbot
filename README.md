# Healthbot — Telegram Bot for Site Monitoring

[![python](https://img.shields.io/badge/Python-3.13-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)  
[![Poetry Version](https://img.shields.io/badge/poetry-2.1.3-blue?logo=python&style=flat-square)](https://python-poetry.org/)  
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)  
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)  
![Docker Image Size](https://img.shields.io/badge/docker-image_~366MB-blue?style=flat-square&logo=docker)

---

## Description

BlumenHorizon Healthbot is a Telegram bot for monitoring website statuses.  
The code is well decomposed, strictly typed (using mypy), and works with MySQL and Redis for persistent and temporary data respectively.

---

## Technologies and Stack

- Python with dependency management via [Poetry 2.1.3](https://python-poetry.org/)  
- Full type coverage with [mypy strict mode](https://mypy-lang.org/)  
- Lightweight `Justfile` for task automation  
- Logging with [Loguru](https://github.com/Delgan/loguru), saving logs to `src/logs/bot.log`  
- Code formatting: `black`, `isort`, `autoflake`

---

## Size and Quality

- The main application container weighs about **366 MB**  
- The code has been manually tested for website interactions  
- The code is well structured, but there is room for improvements  

---

## Configuration — `.env.example`

```env
### --- Telegram Bot Configuration ---
BOT_TOKEN="1111111111:AAAAA-aaaaaaaaaaaaaa-aaaaaaaaa"
TELEGRAM_ADMINS="1111111111;122222222"           # List of Telegram user IDs separated by ;
ALLOWED_CHAT_IDS="-1111111111111;-333333333333"  # List of allowed chat/group IDs separated by ;

### --- Application Mode ---
MODE="PROD"  # or "DEV"

### --- MySQL Configuration ---
MYSQL_DATABASE=healthbot
MYSQL_USER=healthbot_user
MYSQL_PASSWORD=healthbot_pass
MYSQL_ROOT_PASSWORD=healthbot_root_pass
MYSQL_PORT=3306
MYSQL_HOST=mysql

### --- Redis Configuration ---
REDIS_URL="redis://redis:6379"

### --- Logger Configuration ---
LOGURU_LOGS_LEVEL=DEBUG
