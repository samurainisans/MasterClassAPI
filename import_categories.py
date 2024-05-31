import json
import os
import django
from pathlib import Path

# Установка корневой директории проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Установка настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MasterClassAPI.settings')
django.setup()

from apps.masterclasses.models import Category

# Путь к файлу с категориями
file_path = "categories.json"

# Чтение данных из файла
with open(file_path, 'r', encoding='utf-8') as file:
    categories = json.load(file)

# Вставка категорий в базу данных
for category_name in categories:
    category, created = Category.objects.get_or_create(name=category_name)
    if created:
        print(f'Successfully created category: {category_name}')
    else:
        print(f'Category already exists: {category_name}')
