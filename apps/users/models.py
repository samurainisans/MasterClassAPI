# C:/Users/Nik/Desktop/DjangoBackendMasterclases/MasterClassAPI/apps/users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class User(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, blank=True)
    bio = models.TextField(blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=(('male', 'Male'), ('female', 'Female'), ('other', 'Other')),
                              null=True, blank=True)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Contact(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='contact')
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    telegram = models.CharField(max_length=100, null=True, blank=True)
    whatsapp = models.CharField(max_length=100, null=True, blank=True)
    viber = models.CharField(max_length=100, null=True, blank=True)
    vk = models.CharField(max_length=100, null=True, blank=True)
    ok = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.username
