# C:/Users/Nik/Desktop/DjangoBackendMasterclases/MasterClassAPI/generate_user_avatars.py

import os
import django
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# Установка настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MasterClassAPI.settings')
django.setup()

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from apps.users.models import User
from django.conf import settings

PICSUM_URL = 'https://picsum.photos/100'

def get_image_from_picsum():
    try:
        response = requests.get(PICSUM_URL)
        if response.status_code == 200:
            return response.content
    except requests.RequestException as e:
        print(f'Request failed: {e}')
    return None

def save_image_to_server(image_content, filename):
    path = os.path.join('profile_images', filename)
    saved_path = default_storage.save(path, ContentFile(image_content))
    return os.path.join(settings.MEDIA_URL, saved_path.lstrip('/'))

def update_user_with_avatar(user):
    image_content = get_image_from_picsum()
    if image_content:
        filename = f'user_{user.id}.jpg'
        user.image.save(filename, ContentFile(image_content), save=True)
        print(f'Successfully updated user with id: {user.id} with avatar')
        return user.id
    else:
        print(f'Failed to update user with id: {user.id}')
        return None

# Получение всех пользователей без аватарок
users_without_avatars = User.objects.filter(image='')

# Создание пула потоков для параллельного выполнения
with ThreadPoolExecutor(max_workers=50) as executor:
    futures = [executor.submit(update_user_with_avatar, user) for user in users_without_avatars]

    for future in as_completed(futures):
        user_id = future.result()
        if user_id:
            print(f'Avatar updated for user with id: {user_id}')
        else:
            print('Avatar update failed')
