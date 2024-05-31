# masterclasses/models.py
from django.db import models
from django.contrib.auth import get_user_model
from ..users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# доп нагенерить в json:
# duration
# start_date,end_register_date
#
#
# так же шаги для заполнения бд
# сначала заполнить базу ролей, всего их 4
# 1.заполнить базу с пользователями (организаторы, спикеры, админы, участники)
# 2. заполнить базу с категориями
# 3. заполнить базу с мастерклассами
#
#
#
class MasterClass(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    duration = models.PositiveIntegerField()  # duration in minutes
    end_register_date = models.DateTimeField()
    categories = models.ManyToManyField(Category, related_name='masterclasses')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    image = models.ImageField(upload_to='masterclass_images/', null=True, blank=True)
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

    def __str__(self):
        return self.title


class UserMasterClass(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    master_class = models.ForeignKey(MasterClass, on_delete=models.CASCADE)
    register_state = models.CharField(max_length=50)
    date_register = models.DateTimeField(auto_now_add=True)


class FavoriteMasterClass(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    master_class = models.ForeignKey(MasterClass, on_delete=models.CASCADE)


class Participant(models.Model):
    user = models.ForeignKey(User, related_name='participating_masterclasses', on_delete=models.CASCADE)
    masterclass = models.ForeignKey(MasterClass, related_name='participants', on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.masterclass}'

#
# {
#     "password": [
#         "This field may not be blank."
#     ],
#     "username": [
#         "This field may not be blank."
#     ],
#     "first_name": [
#         "This field may not be blank."
#     ],
#     "last_name": [
#         "This field may not be blank."
#     ],
#     "email": [
#         "This field may not be blank."
#     ]
# }

#
# {
#     "title": [
#         "This field may not be blank."
#     ],
#     "description": [
#         "This field may not be blank."
#     ],
#     "start_date": [
#         "Datetime has wrong format. Use one of these formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z]."
#     ],
#     "duration": [
#         "A valid integer is required."
#     ],
#     "end_register_date": [
#         "Datetime has wrong format. Use one of these formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z]."
#     ],
#     "location_name": [
#         "This field may not be blank."
#     ],
#     "country": [
#         "This field may not be blank."
#     ],
#     "street": [
#         "This field may not be blank."
#     ],
#     "house": [
#         "This field may not be blank."
#     ],
#     "postal_code": [
#         "This field may not be blank."
#     ],
#     "categories": [
#         "This list may not be empty."
#     ]
# }