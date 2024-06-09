# C:/Users/Nik/Desktop/DjangoBackendMasterclases/MasterClassAPI/tests/test_masterclass_views.py
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.masterclasses.models import Category, MasterClass, Participant

@pytest.mark.django_db
def test_get_all_masterclasses():
    client = APIClient()
    url = reverse('masterclass-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_get_all_categories():
    client = APIClient()
    url = reverse('categories-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_get_participants_in_masterclass():
    client = APIClient()
    user = get_user_model().objects.create_user(username='testuser', password='12345')
    masterclass = MasterClass.objects.create(
        title="Test MasterClass",
        description="This is a test masterclass",
        start_date="2024-06-10T10:00:00Z",
        end_date="2024-06-10T12:00:00Z",
        duration=120,
        end_register_date="2024-06-09T10:00:00Z",
        organizer=user,
        speaker=user,
        location_name="Test Location",
        country="Test Country",
        street="Test Street",
        house="123",
        postal_code="12345"
    )
    Participant.objects.create(user=user, masterclass=masterclass)
    url = reverse('masterclass-participants', args=[masterclass.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_get_cities():
    client = APIClient()
    url = reverse('cities-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_filter_masterclasses_by_categories():
    client = APIClient()
    user = get_user_model().objects.create_user(username='testuser', password='12345')
    category1 = Category.objects.create(name="Category 1")
    category2 = Category.objects.create(name="Category 2")
    masterclass = MasterClass.objects.create(
        title="Test MasterClass",
        description="This is a test masterclass",
        start_date="2024-06-10T10:00:00Z",
        end_date="2024-06-10T12:00:00Z",
        duration=120,
        end_register_date="2024-06-09T10:00:00Z",
        organizer=user,
        speaker=user,
        location_name="Test Location",
        country="Test Country",
        street="Test Street",
        house="123",
        postal_code="12345"
    )
    masterclass.categories.add(category1, category2)
    url = f"{reverse('masterclass-list')}?categories={category1.id}&categories={category2.id}"
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_filter_masterclasses_by_locality():
    client = APIClient()
    user = get_user_model().objects.create_user(username='testuser', password='12345')
    category = Category.objects.create(name="Test Category")
    masterclass = MasterClass.objects.create(
        title="Test MasterClass",
        description="This is a test masterclass",
        start_date="2024-06-10T10:00:00Z",
        end_date="2024-06-10T12:00:00Z",
        duration=120,
        end_register_date="2024-06-09T10:00:00Z",
        organizer=user,
        speaker=user,
        location_name="Test Location",
        country="Test Country",
        street="Test Street",
        house="123",
        postal_code="12345",
        locality="Санкт-Петербург"
    )
    masterclass.categories.add(category)
    url = f"{reverse('masterclass-list')}?locality=Санкт-Петербург"
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_filter_masterclasses_by_time():
    client = APIClient()
    user = get_user_model().objects.create_user(username='testuser', password='12345')
    category = Category.objects.create(name="Test Category")
    masterclass = MasterClass.objects.create(
        title="Test MasterClass",
        description="This is a test masterclass",
        start_date="2024-06-10T10:00:00Z",
        end_date="2024-06-10T12:00:00Z",
        duration=120,
        end_register_date="2024-06-09T10:00:00Z",
        organizer=user,
        speaker=user,
        location_name="Test Location",
        country="Test Country",
        street="Test Street",
        house="123",
        postal_code="12345"
    )
    masterclass.categories.add(category)
    url = f"{reverse('masterclass-list')}?start_date=2024-06-02T00:00:00&end_date=2024-06-15T23:59:59"
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_filter_masterclasses_by_combination():
    client = APIClient()
    user = get_user_model().objects.create_user(username='testuser', password='12345')
    category = Category.objects.create(name="Category 1")
    masterclass = MasterClass.objects.create(
        title="Test MasterClass",
        description="This is a test masterclass",
        start_date="2024-06-10T10:00:00Z",
        end_date="2024-06-10T12:00:00Z",
        duration=120,
        end_register_date="2024-06-09T10:00:00Z",
        organizer=user,
        speaker=user,
        location_name="Test Location",
        country="Test Country",
        street="Test Street",
        house="123",
        postal_code="12345",
        locality="Москва"
    )
    masterclass.categories.add(category)
    url = f"{reverse('masterclass-list')}?categories={category.id}&locality=Москва&start_date=2024-06-02T00:00:00&end_date=2024-06-15T23:59:59"
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_search_masterclasses():
    client = APIClient()
    user = get_user_model().objects.create_user(username='testuser', password='12345')
    category = Category.objects.create(name="Test Category")
    masterclass = MasterClass.objects.create(
        title="Test MasterClass",
        description="This is a test masterclass",
        start_date="2024-06-10T10:00:00Z",
        end_date="2024-06-10T12:00:00Z",
        duration=120,
        end_register_date="2024-06-09T10:00:00Z",
        organizer=user,
        speaker=user,
        location_name="Test Location",
        country="Test Country",
        street="Test Street",
        house="123",
        postal_code="12345"
    )
    masterclass.categories.add(category)
    url = f"{reverse('masterclass-list')}?search=программирование"
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_create_masterclass():
    client = APIClient()
    user = get_user_model().objects.create_user(username='testuser', password='12345')
    category = Category.objects.create(name="Test Category")
    url = reverse('masterclass-list')
    data = {
        "title": "Test MasterClass",
        "description": "This is a test masterclass",
        "start_date": "2024-06-17T17:47:20Z",
        "end_date": "2024-06-17T18:51:20Z",
        "duration": 64,
        "end_register_date": "2024-06-25T00:00:00Z",
        "categories": [category.id],
        "longitude": "49.416333",
        "latitude": "53.511499",
        "image_url": "https://images.unsplash.com/photo-1709060912378-abc334fbcfa0?crop=entropy&cs=tinysrgb&fit=crop&fm=jpg&h=300&ixid=MnwxfDB8MXxyYW5kb218MHx8fHx8fHx8MTcxNzIzMTE3Mg&ixlib=rb-4.0.3&q=80&w=400",
        "organizer": user.id,
        "speaker": user.id,
        "location_name": "Тольятти, ул Гагарина, д. 4",
        "country": "Россия",
        "province": "Самарская область",
        "area": "городской округ Тольятти",
        "locality": "Тольятти",
        "street": "улица Гагарина",
        "house": "4",
        "postal_code": "445017"
    }
    client.force_authenticate(user=user)
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
