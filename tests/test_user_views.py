# C:/Users/Nik/Desktop/DjangoBackendMasterclases/MasterClassAPI\tests\test_user_views.py
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.users.models import Role

@pytest.mark.django_db
def test_get_all_users():
    client = APIClient()
    url = reverse('user-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_confirm_account():
    client = APIClient()
    url = reverse('activate', args=['MTg0', 'c87nqu-346194cfef5de6dcc654ea07781217a2'])
    response = client.get(url)
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]

@pytest.mark.django_db
def test_get_organizers():
    client = APIClient()
    url = reverse('user-get-organizers')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_get_speakers():
    client = APIClient()
    url = reverse('user-get-speakers')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_register_user():
    client = APIClient()
    url = reverse('register')
    role = Role.objects.create(name='Test Role')
    data = {
        "username": "Valeriya",
        "email": "aressamurai@mail.ru",
        "password": "sdjfksdk239423",
        "first_name": "Lera",
        "last_name": "Lavr",
        "role": role.id
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert get_user_model().objects.filter(username='Valeriya').exists()

@pytest.mark.django_db
def test_login_user():
    client = APIClient()
    user = get_user_model().objects.create_user(username='Valeriya', password='sdjfksdk239423')
    url = reverse('token_obtain_pair')
    data = {
        "username": "Valeriya",
        "password": "sdjfksdk239423"
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_refresh_token():
    client = APIClient()
    user = get_user_model().objects.create_user(username='Valeriya', password='sdjfksdk239423')
    refresh_token = client.post(reverse('token_obtain_pair'), {"username": "Valeriya", "password": "sdjfksdk239423"}, format='json').data['refresh']
    url = reverse('token_refresh')
    data = {
        "refresh": refresh_token
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
