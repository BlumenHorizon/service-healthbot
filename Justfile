default:
    @echo "Available commands:"
    @just --summary

# === Project-specific commands ===

migrate:
    python3 -m src.db.init_db

telegram:
    python3 -m src.main

# === Code formatting & linting ===

fmt:
    black .

autoflake:
    autoflake .

isort:
    isort .

lint: autoflake isort fmt

clean:
    find . -type d -name "__pycache__" -exec rm -r {} +

# === Docker Compose commands ===

up:
    docker compose up -d

down:
    docker compose down

restart:
    docker compose restart

rebuild:
    docker compose up --build -d

stop:
    docker compose stop

start:
    docker compose start