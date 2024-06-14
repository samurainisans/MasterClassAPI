# masterclasses/models.py
from django.db import models
from ..users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MasterClass(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    duration = models.PositiveIntegerField()
    end_register_date = models.DateTimeField()
    categories = models.ManyToManyField(Category, related_name='masterclasses')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    image_url = models.ImageField(upload_to='masterclass_images/', null=True, blank=True)
    organizer = models.ForeignKey(User, related_name='organized_masterclasses', on_delete=models.CASCADE)
    speaker = models.ForeignKey(User, related_name='speaking_masterclasses', on_delete=models.CASCADE)
    location_name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    province = models.CharField(max_length=255, null=True, blank=True)
    area = models.CharField(max_length=255, null=True, blank=True)
    locality = models.CharField(max_length=255, null=True, blank=True)
    street = models.CharField(max_length=255)
    house = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    requires_approval = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.title



class UserMasterClass(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    master_class = models.ForeignKey(MasterClass, on_delete=models.CASCADE)
    register_state = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    date_register = models.DateTimeField(auto_now_add=True)



class FavoriteMasterClass(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    master_class = models.ForeignKey(MasterClass, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} - {self.master_class}'


class Participant(models.Model):
    user = models.ForeignKey(User, related_name='participating_masterclasses', on_delete=models.CASCADE)
    masterclass = models.ForeignKey(MasterClass, related_name='participants', on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.masterclass}'
