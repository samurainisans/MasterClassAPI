# admin.py
from django.contrib import admin
from .models import Category, MasterClass, Participant, Speaker, Organizer

admin.site.register(Category)
admin.site.register(MasterClass)
admin.site.register(Participant)
admin.site.register(Speaker)
admin.site.register(Organizer)
