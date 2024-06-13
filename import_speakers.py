import json
import os
import django
from pathlib import Path
from django.contrib.auth.hashers import make_password

# Установка настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MasterClassAPI.settings')
django.setup()

from apps.users.models import User, Role

# Путь к файлу со спикерами
base_dir = Path(__file__).resolve().parent
file_path = 'speakers.json'

# Чтение данных из файла
with open(file_path, 'r', encoding='utf-8') as file:
    speakers = json.load(file)

# Получение роли "Speaker"
speaker_role = Role.objects.get(name='Speaker')
# Вставка спикеров в базу данных
for speaker in speakers:
    name_parts = speaker['name'].split()
    first_name = name_parts[0]
    last_name = name_parts[1] if len(name_parts) > 1 else ''

    user, created = User.objects.get_or_create(
        username=speaker['name'].replace(" ", "").lower(),
        defaults={
            'first_name': first_name,
            'last_name': last_name,
            'email': f"{speaker['name'].replace(' ', '').lower()}@example.com",
            'password': make_password('defaultpassword'),
            'role': speaker_role,
        }
    )
    if created:
        print(f'Successfully created user: {speaker["name"]}')
    else:
        print(f'User already exists: {speaker["name"]}')
