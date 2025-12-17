#!/bin/sh

# Применяем миграции
echo "Применение миграций Alembic..."
alembic upgrade head

echo "Создаем админа..."
python create_admin.py

# Запускаем приложение
echo "Запуск приложения..."
exec uvicorn backend.src.main:app --host 0.0.0.0 --port 8000
