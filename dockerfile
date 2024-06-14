# используем официальный образ python 3.11
FROM python:3.11-slim

# устанавливаем зависимости для psycopg2 и других необходимых библиотек
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev python3-dev netcat-traditional && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# устанавливаем рабочую директорию
WORKDIR /app

# копируем и устанавливаем зависимости
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# копируем файлы проекта
COPY . /app/

# сборка статических файлов
RUN python manage.py collectstatic --noinput

# настраиваем переменные окружения
ENV PYTHONUNBUFFERED 1

# копируем скрипт entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# команда запуска
CMD ["/entrypoint.sh"]