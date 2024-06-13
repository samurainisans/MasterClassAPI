#!/bin/sh

# Функция для проверки доступности PostgreSQL
check_postgres() {
  python << END
import sys
import psycopg2
from psycopg2 import OperationalError

try:
    conn = psycopg2.connect(
        dbname="${DB_NAME}",
        user="${DB_USER}",
        password="${DB_PASSWORD}",
        host="${DB_HOST}",
        port="${DB_PORT}"
    )
except OperationalError:
    sys.exit(1)
sys.exit(0)
END
}

# Ждем, пока PostgreSQL станет доступным
until check_postgres; do
  echo "Waiting for the PostgreSQL server to start..."
  sleep 1
done

# Применение миграций базы данных
python manage.py migrate

# Сборка статических файлов
python manage.py collectstatic --noinput

# Запуск приложения
exec "$@"