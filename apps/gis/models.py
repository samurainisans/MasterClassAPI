# gis/models.py
from django.db import models
from ..masterclasses.models import MasterClass, Participant


class GISMasterClass(MasterClass):
    participants = models.ManyToManyField(Participant, blank=True, related_name='gis_masterclasses')

    class Meta:
        verbose_name = 'GIS Мастер-класс'
        verbose_name_plural = 'GIS Мастер-классы'


