import os
import django
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

# Установка настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MasterClassAPI.settings')
django.setup()

from apps.masterclasses.models import MasterClass
from django.conf import settings

# Конфигурация статической ссылки Picsum
PICSUM_URL = 'https://picsum.photos/400/300'

def get_image_url():
    try:
        response = requests.get(PICSUM_URL)
        if response.status_code == 200:
            return response.content
    except requests.RequestException as e:
        print(f'Request failed: {e}')
    return None

def save_image_to_server(image_content, filename):
    path = os.path.join('masterclass_images', filename)
    saved_path = default_storage.save(path, ContentFile(image_content))
    return os.path.join(settings.MEDIA_URL, saved_path.lstrip('/'))

def update_masterclass_with_image(masterclass):
    image_content = get_image_url()
    if image_content:
        filename = f'masterclass_{masterclass.id}.jpg'
        image_url = save_image_to_server(image_content, filename)
        masterclass.image_url = image_url
        masterclass.save()
        return masterclass.id, image_url
    return masterclass.id, None

# Получение всех мастер-классов
masterclasses = MasterClass.objects.all()

# Создание пула потоков для параллельного выполнения
with ThreadPoolExecutor(max_workers=50) as executor:
    futures = [executor.submit(update_masterclass_with_image, mc) for mc in masterclasses]

    for future in as_completed(futures):
        mc_id, image_url = future.result()
        if image_url:
            print(f'Successfully updated masterclass with id: {mc_id} with image url: {image_url}')
        else:
            print(f'Failed to get image for masterclass with id: {mc_id}')
