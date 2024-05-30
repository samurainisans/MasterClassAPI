from django.contrib import admin
from .models import User, Role, Contact

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'verified')
    search_fields = ('username', 'email', 'first_name', 'last_name')

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'telegram', 'whatsapp', 'viber', 'vk', 'ok')
    search_fields = ('user__username', 'phone_number', 'telegram', 'whatsapp', 'viber', 'vk', 'ok')
