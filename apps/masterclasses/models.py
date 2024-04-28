#masterclasses/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Organizer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    contact_info = models.CharField(max_length=255, null=True, blank=True)
    logo = models.ImageField(upload_to='organizer_logos/', null=True, blank=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class AbstractEvent(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    location_name = models.CharField(max_length=255, verbose_name="Название места")
    latitude = models.FloatField(null=True, blank=True, verbose_name="Широта")
    longitude = models.FloatField(null=True, blank=True, verbose_name="Долгота")
    start_time = models.DateTimeField(verbose_name="Время начала")
    end_time = models.DateTimeField(null=True, blank=True, verbose_name="Время окончания")
    registration_deadline = models.TextField(verbose_name="Крайний срок регистрации")
    class Meta:
        abstract = True

    def __str__(self):
        return self.title

class Speaker(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    profile_image = models.ImageField(upload_to='speaker_profiles/', null=True, blank=True)
    masterclass = models.ForeignKey('MasterClass', related_name='masterclass_speakers', on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.name} ({self.title})'


class MasterClass(AbstractEvent):
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE, related_name='organized_masterclasses', verbose_name="Организатор")
    categories = models.ManyToManyField(Category, verbose_name="Категории")
    speakers = models.ManyToManyField(Speaker, related_name='masterclasses', verbose_name="Спикеры")
    class Meta:
        verbose_name = 'Мастер-класс'
        verbose_name_plural = 'Мастер-классы'


class Participant(models.Model):
    user = models.ForeignKey(User, related_name='participating_masterclasses', on_delete=models.CASCADE)
    masterclass = models.ForeignKey(MasterClass, related_name='participants', on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.masterclass}'
