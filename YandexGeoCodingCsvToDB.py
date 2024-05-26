import os

import pandas as pd
from django.db.models import Q
import django
df = pd.read_csv('complete_coordinates.csv')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MasterClassAPI.settings')
django.setup()

from apps.gis.models import GISMasterClass

def update_gis_masterclass_coordinates():
    updated_count = 0
    for index, row in df.iterrows():
        masterclass_objects = GISMasterClass.objects.filter(
            Q(location_name__iexact=row['address']) |
            Q(location_name__icontains=row['address'])
        )

        for masterclass in masterclass_objects:
            if masterclass.latitude is None and masterclass.longitude is None:
                masterclass.latitude = float(row['latitude'])
                masterclass.longitude = float(row['longitude'])
                masterclass.save()
                updated_count += 1
    return updated_count

# Вызов функции и печать результатов
updated_count = update_gis_masterclass_coordinates()
print(f'Updated coordinates for {updated_count} GIS MasterClasses')

