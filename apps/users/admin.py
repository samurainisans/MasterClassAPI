# users/admin.py

from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from .models import Role, User

admin.site.register(Role)
admin.site.register(User)


def create_groups_and_permissions():
    roles = ['Admin', 'Organizer', 'Speaker', 'Participant']

    for role in roles:
        group, created = Group.objects.get_or_create(name=role)

        if role == 'Admin':
            permissions = Permission.objects.all()
        elif role == 'Organizer':
            permissions = Permission.objects.filter(codename__in=[
                'add_masterclass', 'change_masterclass', 'delete_masterclass', 'view_masterclass',
                'add_usermasterclass', 'change_usermasterclass', 'delete_usermasterclass', 'view_usermasterclass'
            ])
        elif role == 'Speaker':
            permissions = Permission.objects.filter(codename__in=[
                'view_masterclass', 'add_favoritemasterclass', 'delete_favoritemasterclass', 'view_usermasterclass'
            ])
        elif role == 'Participant':
            permissions = Permission.objects.filter(codename__in=[
                'view_masterclass', 'add_favoritemasterclass', 'delete_favoritemasterclass', 'view_favoritemasterclass'
            ])

        group.permissions.set(permissions)
        group.save()


create_groups_and_permissions()
