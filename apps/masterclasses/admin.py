from django.contrib import admin
from .models import MasterClass, Category, UserMasterClass, FavoriteMasterClass

@admin.register(MasterClass)
class MasterClassAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'organizer', 'location_name', 'country')
    search_fields = ('title', 'organizer__username', 'location_name', 'country')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(UserMasterClass)
class UserMasterClassAdmin(admin.ModelAdmin):
    list_display = ('user', 'master_class', 'register_state', 'date_register')
    search_fields = ('user__username', 'master_class__title', 'register_state')

@admin.register(FavoriteMasterClass)
class FavoriteMasterClassAdmin(admin.ModelAdmin):
    list_display = ('user', 'master_class')
    search_fields = ('user__username', 'master_class__title')
