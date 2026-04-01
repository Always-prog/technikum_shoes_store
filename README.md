# Technikum Shoes Store (MVP)

Учебный интернет-магазин обуви на Flask с PostgreSQL и MinIO в Docker.

## Стек

- Python + Flask
- Jinja2 templates + HTML/CSS
- SQLAlchemy + PostgreSQL
- MinIO (S3-совместимое хранилище изображений)
- Docker Compose

## Быстрый старт

1. Подготовь окружение:
   ```bash
   cp .env.example .env
   ```
2. Запусти сервисы:
   ```bash
   docker compose up -d --build
   ```
3. Наполни демо-данными:
   ```bash
   docker compose exec web flask seed-demo
   ```
4. Открой:
   - Приложение: `http://localhost:5000`
   - MinIO console: `http://localhost:9001`

## Полезные команды

- Пересобрать и запустить: `docker compose up -d --build`
- Логи web: `docker compose logs web -f`
- Остановить: `docker compose down`
