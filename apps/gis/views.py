# gis/views.py
import requests
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response


class GISMasterClassViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'], url_path='geocode')
    def geocode(self, request):
        location_name = request.query_params.get('location_name')
        if not location_name:
            return Response({'error': 'адрес не предоставлен'}, status=status.HTTP_400_BAD_REQUEST)

        response = requests.get(
            'https://geocode-maps.yandex.ru/1.x',
            params={
                'apikey': '9a12263e-fb61-48d8-a9ce-01408b803f37',
                'geocode': location_name,
                'format': 'json'
            }
        )
        data = response.json()
        if not data['response']['GeoObjectCollection']['featureMember']:
            return Response({'error': 'адрес не найден'}, status=status.HTTP_404_NOT_FOUND)

        geo_object = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
        pos = geo_object['Point']['pos']
        longitude, latitude = map(float, pos.split())
        address_components = geo_object['metaDataProperty']['GeocoderMetaData']['Address']['Components']

        address_dict = {component['kind']: component['name'] for component in address_components}
        country = address_dict.get('country', '')
        province = address_dict.get('province', '')
        area = address_dict.get('area', '')
        locality = address_dict.get('locality', '')
        street = address_dict.get('street', '')
        house = address_dict.get('house', '')
        postal_code = geo_object['metaDataProperty']['GeocoderMetaData']['Address'].get('postal_code', '')

        response_data = {
            'longitude': longitude,
            'latitude': latitude,
            'location_name': location_name,
            'country': country,
            'province': province,
            'area': area,
            'locality': locality,
            'street': street,
            'house': house,
            'postal_code': postal_code
        }

        return Response(response_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='reverse-geocode')
    def reverse_geocode(self, request):
        longitude = request.query_params.get('longitude')
        latitude = request.query_params.get('latitude')
        if not longitude or not latitude:
            return Response({'error': 'координаты не предоставлены'}, status=status.HTTP_400_BAD_REQUEST)

        response = requests.get(
            'https://geocode-maps.yandex.ru/1.x',
            params={
                'apikey': '9a12263e-fb61-48d8-a9ce-01408b803f37',
                'geocode': f'{longitude},{latitude}',
                'format': 'json',
                'kind': 'house'
            }
        )
        data = response.json()
        if not data['response']['GeoObjectCollection']['featureMember']:
            return Response({'error': 'адрес не найден'}, status=status.HTTP_404_NOT_FOUND)

        geo_object = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
        address_components = geo_object['metaDataProperty']['GeocoderMetaData']['Address']['Components']

        address_dict = {component['kind']: component['name'] for component in address_components}
        country = address_dict.get('country', '')
        province = address_dict.get('province', '')
        area = address_dict.get('area', '')
        locality = address_dict.get('locality', '')
        street = address_dict.get('street', '')
        house = address_dict.get('house', '')
        postal_code = geo_object['metaDataProperty']['GeocoderMetaData']['Address'].get('postal_code', '')

        response_data = {
            'longitude': longitude,
            'latitude': latitude,
            'country': country,
            'province': province,
            'area': area,
            'locality': locality,
            'street': street,
            'house': house,
            'postal_code': postal_code
        }

        return Response(response_data, status=status.HTTP_200_OK)
