import os
import json
from datetime import datetime
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MasterClassAPI.settings')
django.setup()

from apps.masterclasses.models import MasterClass, Category, Organizer, Speaker

json_path = 'masterclasses1.2.json'
with open(json_path, 'r', encoding='utf-8') as file:
    masterclasses = json.load(file)

def parse_datetime_from_json(date_str):
    if not date_str:
        return datetime.now()  # Используем текущее время по умолчанию
    months = {
        'января': '01', 'февраля': '02', 'марта': '03',
        'апреля': '04', 'мая': '05', 'июня': '06',
        'июля': '07', 'августа': '08', 'сентября': '09',
        'октября': '10', 'ноября': '11', 'декабря': '12'
    }
    parts = date_str.split()
    day = int(parts[0])
    month_name = parts[1].replace(',', '')
    month = months.get(month_name, '01')  # Если месяц не найден, используем январь по умолчанию
    year = datetime.now().year  # Предполагаем текущий год
    time = '12:00'  # Фиксированное время
    try:
        return datetime.strptime(f"{year} {month} {day} {time}", "%Y %m %d %H:%M")
    except ValueError:
        print(f"Неверная дата: {day} {month_name}. Используем текущее время.")
        return datetime.now()

for mc in masterclasses:
    organizer_info = mc['organizer']
    organizer_name = organizer_info.get('name', 'Иванов Иван')
    organizer, _ = Organizer.objects.get_or_create(
        name=organizer_name,
        defaults={'logo': organizer_info.get('logo', '')}
    )
    categories = [Category.objects.get_or_create(name=cat)[0] for cat in mc.get('categories', [])]
    start_time = parse_datetime_from_json(mc.get('start_time', ''))
    end_time = parse_datetime_from_json(mc.get('end_time', ''))

    new_masterclass = MasterClass.objects.create(
        title=mc['title'],
        description=mc['description'],
        location_name=mc['location_name'],
        latitude=mc.get('latitude', None),
        longitude=mc.get('longitude', None),
        start_time=start_time,
        end_time=end_time,
        registration_deadline=mc['registration_deadline'],
        organizer=organizer
    )
    new_masterclass.categories.set(categories)

    for speaker_info in mc.get('speakers', []):
        Speaker.objects.create(
            name=speaker_info['name'],
            title=speaker_info.get('title', ''),
            profile_image=speaker_info.get('image', ''),
            masterclass=new_masterclass
        )

print("Импорт данных выполнен успешно!")
