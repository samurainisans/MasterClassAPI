import json
import os
import django
import random
from pathlib import Path
from django.utils import timezone

# Установка настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MasterClassAPI.settings')
django.setup()

from apps.masterclasses.models import MasterClass, Category
from apps.users.models import User

# Путь к файлу с мастер-классами
base_dir = Path(__file__).resolve().parent
file_path = 'enriched_masterclasses.json'

# Чтение данных из файла
with open(file_path, 'r', encoding='utf-8') as file:
    masterclasses = json.load(file)

# Получение организатора
organizer = User.objects.get(id=181)

# Получение всех пользователей с ролью "Speaker"
speakers = User.objects.get(name='Speaker')
# Функция для генерации цены
def generate_price():
    price = random.randint(1500, 3000)
    return round(price / 100) * 100

# Вставка мастер-классов в базу данных
for mc in masterclasses:
    # Выбор случайного спикера
    speaker = random.choice(speakers)

    # Обработка naive datetime
    start_date = timezone.make_aware(timezone.datetime.strptime(mc['start_date'], '%Y-%m-%dT%H:%M:%S'))
    end_date = timezone.make_aware(timezone.datetime.strptime(mc['end_date'], '%Y-%m-%dT%H:%M:%S'))
    end_register_date = timezone.make_aware(timezone.datetime.strptime(mc['end_register_date'], '%Y-%m-%dT%H:%M:%S'))

    # Генерация цены
    price = generate_price()

    # Создание мастер-класса
    masterclass = MasterClass.objects.create(
        title=mc['title'],
        description=mc['description'],
        start_date=start_date,
        end_date=end_date,
        duration=mc['duration'],
        end_register_date=end_register_date,
        longitude=mc.get('coordinates', {}).get('longitude'),
        latitude=mc.get('coordinates', {}).get('latitude'),
        location_name=mc.get('location_name', ''),
        country=mc.get('country', ''),
        province=mc.get('province', ''),
        area=mc.get('area', ''),
        locality=mc.get('locality', ''),
        street=mc.get('street', ''),
        house=mc.get('house', ''),
        postal_code=mc.get('postal_code', ''),
        organizer=organizer,
        speaker=speaker,
        price=price
    )

    # Добавление категорий к мастер-классу
    for category_name in mc['categories']:
        category = Category.objects.get(name=category_name)
        masterclass.categories.add(category)

    masterclass.save()
    print(f'Successfully created masterclass: {mc["title"]} with price {price}')
