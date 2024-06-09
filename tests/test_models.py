# C:/Users/Nik/Desktop/DjangoBackendMasterclases/MasterClassAPI\tests\test_models.py
import pytest
from django.contrib.auth import get_user_model
from apps.masterclasses.models import Category, MasterClass, UserMasterClass, FavoriteMasterClass, Participant

@pytest.mark.django_db
def test_category_model():
    category = Category.objects.create(name="Test Category")
    assert category.name == "Test Category"

@pytest.mark.django_db
def test_masterclass_model():
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
    assert masterclass.title == "Test MasterClass"
    assert masterclass.categories.count() == 1

@pytest.mark.django_db
def test_usermasterclass_model():
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
    user_masterclass = UserMasterClass.objects.create(user=user, master_class=masterclass, register_state="pending")
    assert user_masterclass.user == user
    assert user_masterclass.master_class == masterclass
    assert user_masterclass.register_state == "pending"

@pytest.mark.django_db
def test_favoritemasterclass_model():
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
    favorite_masterclass = FavoriteMasterClass.objects.create(user=user, master_class=masterclass)
    assert favorite_masterclass.user == user
    assert favorite_masterclass.master_class == masterclass

@pytest.mark.django_db
def test_participant_model():
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
    participant = Participant.objects.create(user=user, masterclass=masterclass)
    assert participant.user == user
    assert participant.masterclass == masterclass
