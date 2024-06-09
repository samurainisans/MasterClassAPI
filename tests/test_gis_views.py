# C:/Users/Nik/Desktop/DjangoBackendMasterclases/MasterClassAPI/tests/test_gis_views.py
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch

@pytest.mark.django_db
def test_geocode_address_provided():
    client = APIClient()
    url = reverse('gis-masterclass-geocode')
    params = {'location_name': 'Москва, ул. Арбат, 10'}

    # mock the requests.get call to return a fake response
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {
            'response': {
                'GeoObjectCollection': {
                    'featureMember': [{
                        'GeoObject': {
                            'Point': {'pos': '37.6056 55.7403'},
                            'metaDataProperty': {
                                'GeocoderMetaData': {
                                    'Address': {
                                        'Components': [
                                            {'kind': 'country', 'name': 'Россия'},
                                            {'kind': 'province', 'name': 'Москва'},
                                            {'kind': 'locality', 'name': 'Москва'},
                                            {'kind': 'street', 'name': 'Арбат'},
                                            {'kind': 'house', 'name': '10'}
                                        ],
                                        'postal_code': '119019'
                                    }
                                }
                            }
                        }
                    }]
                }
            }
        }
        response = client.get(url, params)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['longitude'] == 37.6056
    assert response.data['latitude'] == 55.7403
    assert response.data['country'] == 'Россия'
    assert response.data['province'] == 'Москва'
    assert response.data['locality'] == 'Москва'
    assert response.data['street'] == 'Арбат'
    assert response.data['house'] == '10'
    assert response.data['postal_code'] == '119019'

@pytest.mark.django_db
def test_geocode_address_not_provided():
    client = APIClient()
    url = reverse('gis-masterclass-geocode')
    response = client.get(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['error'] == 'адрес не предоставлен'

@pytest.mark.django_db
def test_geocode_address_not_found():
    client = APIClient()
    url = reverse('gis-masterclass-geocode')
    params = {'location_name': 'Some non-existing place'}

    # mock the requests.get call to return a fake response
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {
            'response': {
                'GeoObjectCollection': {
                    'featureMember': []
                }
            }
        }
        response = client.get(url, params)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['error'] == 'адрес не найден'
