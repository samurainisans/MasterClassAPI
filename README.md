# Инструкция по развертыванию сервера

Эта инструкция поможет вам развернуть сервер с использованием Docker Compose. Следуйте шагам ниже для настройки и запуска всех необходимых компонентов.

## Предварительные шаги

1. Установите [Docker](https://www.docker.com/products/docker-desktop) и [Docker Compose](https://docs.docker.com/compose/install/).
2. Скачайте или клонируйте проект на ваш локальный компьютер.

## Создание `.env` файла

Создайте файл `.env` в корневой директории проекта и добавьте следующие переменные окружения:

```plaintext
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
```

## Установка зависимостей

Убедитесь, что у вас есть файл `requirements.txt` в корневой директории проекта. Пример содержимого файла `requirements.txt` https://github.com/samurainisans/MasterClassAPI/blob/dev/requirements.txt:

```plaintext
Django==3.2
djangorestframework==3.12.4
gunicorn==20.1.0
psycopg2-binary==2.8.6
```

Эти версии библиотек и пакетов будут установлены при сборке контейнера.

## Docker Compose файл

Убедитесь, что у вас есть следующий `docker-compose.yml` файл в корневой директории проекта:

```yaml
version: '3.9'

services:
  db:
    image: postgres:14
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}

  web:
    build: .
    command: gunicorn MasterClassAPI.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    env_file:
      - .env

  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - ./staticfiles:/app/staticfiles  # убедитесь, что ./staticfiles существует и содержит файлы
      - ./media:/app/media  # убедитесь, что ./media существует и содержит файлы
    depends_on:
      - web

volumes:
  postgres_data:
```

## Настройка и запуск

1. Перейдите в корневую директорию проекта.
2. Запустите Docker Compose командой:

```sh
docker-compose up --build
```

Эта команда соберет и запустит все необходимые контейнеры.

## Проверка работы сервера

После успешного запуска всех сервисов, сервер будет доступен по адресу http://localhost. Проверьте его работоспособность, открыв этот адрес в браузере.

## Дополнительные команды

- Остановка всех контейнеров:

```sh
docker-compose down
```

- Просмотр логов:

```sh
docker-compose logs -f
```

- Перезапуск контейнеров:

```sh
docker-compose restart
```

Теперь ваш сервер развернут и готов к использованию!
