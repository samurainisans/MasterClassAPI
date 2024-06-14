import os
import django

# Установка настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MasterClassAPI.settings')
django.setup()

from apps.users.models import Role

# Роли, которые нужно создать
roles = [
    'Admin',
    'Organizer',
    'Speaker',
    'Participant'
]

# Вставка ролей в базу данных
for role_name in roles:
    role, created = Role.objects.get_or_create(name=role_name)
    if created:
        print(f'Successfully created role: {role_name}')
    else:
        print(f'Role already exists: {role_name}')
