import json

# Загрузите ваш исходный JSON-файл
with open('enriched_masterclasses.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Подготовьте структуру для GeoJSON
geojson = {
    "type": "FeatureCollection",
    "features": []
}

# Преобразуйте каждый элемент в вашем JSON-файле в GeoJSON Feature
for item in data:
    if 'coordinates' in item:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [float(item['coordinates']['longitude']), float(item['coordinates']['latitude'])]
            },
            "properties": item,
        }
        # Удалите координаты из свойств
        del feature['properties']['coordinates']

        # Добавьте Feature в ваш GeoJSON
        geojson['features'].append(feature)

# Сохраните ваш GeoJSON в новый файл
with open('output.geojson', 'w', encoding='utf-8') as f:
    json.dump(geojson, f, ensure_ascii=False)