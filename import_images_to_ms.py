import os
import django
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# Установка настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MasterClassAPI.settings')
django.setup()

from apps.masterclasses.models import MasterClass

# Конфигурация статической ссылки Unsplash
UNSPLASH_URL = 'https://source.unsplash.com/random/400x200'

def get_image_url():
    response = requests.get(UNSPLASH_URL)
    if response.status_code == 200:
        return response.url
    return None

def update_masterclass(masterclass):
    image_url = get_image_url()
    if image_url:
        masterclass.image_url = image_url
        masterclass.save()
        return masterclass.id, image_url
    return masterclass.id, None

# Получение всех мастер-классов
masterclasses = MasterClass.objects.all()

# Создание пула потоков для параллельного выполнения
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(update_masterclass, mc) for mc in masterclasses]

    for future in as_completed(futures):
        mc_id, image_url = future.result()
        if image_url:
            print(f'Successfully updated masterclass with id: {mc_id} with image url: {image_url}')
        else:
            print(f'Failed to get image for masterclass with id: {mc_id}')
