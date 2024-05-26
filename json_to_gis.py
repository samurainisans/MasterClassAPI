import os
import json
import django

# Устанавливаем настройки проекта Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MasterClassAPI.settings')
django.setup()

# Импортируем модели
from apps.gis.models import GISMasterClass
from apps.masterclasses.models import Category, Organizer, Speaker

# Путь к JSON файлу
json_path = 'masterclasses1.2.json'
with open(json_path, 'r', encoding='utf-8') as file:
    masterclasses = json.load(file)

def parse_datetime_from_json(date_str):
    # Возвращаем None, если дата не указана
    return date_str if date_str else None


# Импорт данных в модель GISMasterClass
for mc in masterclasses:
    organizer_info = mc.get('organizer', {})
    organizer, _ = Organizer.objects.get_or_create(
        name=organizer_info.get('name', 'Иванов Иван'),
        defaults={'logo': organizer_info.get('logo', '')}
    )

    categories_objs = [Category.objects.get_or_create(name=category_name)[0] for category_name in
                       mc.get('categories', [])]

    gis_masterclass = GISMasterClass.objects.create(
        title=mc['title'],
        description=mc['description'],
        location_name=mc['location_name'],
        latitude=mc.get('latitude'),
        longitude=mc.get('longitude'),
        start_time=mc.get('start_time'),
        end_time=parse_datetime_from_json(mc.get('end_time')),
        registration_deadline=mc['registration_deadline'],
        organizer=organizer
    )

    gis_masterclass.categories.set(categories_objs)

    for speaker_info in mc.get('speakers', []):
        speakers = Speaker.objects.filter(name=speaker_info['name'], masterclass=gis_masterclass)
        if speakers.exists():
            speaker = speakers.first()
        else:
            speaker = Speaker.objects.create(
                name=speaker_info['name'],
                title=speaker_info.get('title', ''),
                profile_image=speaker_info.get('image', ''),
                masterclass=gis_masterclass
            )
        gis_masterclass.speakers.add(speaker)

print("Импорт данных в GIS выполнен успешно!")
