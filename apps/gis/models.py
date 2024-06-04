# gis/models.py
from ..masterclasses.models import MasterClass


class GISMasterClass(MasterClass):
    class Meta:
        verbose_name = 'GIS Мастер-класс'
        verbose_name_plural = 'GIS Мастер-классы'
