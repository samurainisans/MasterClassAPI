import os
import django

# Установка настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MasterClassAPI.settings')
django.setup()

from django.contrib.auth.models import Permission
from apps.users.models import User


def get_user_permissions():
    users = User.objects.all()
    user_permissions_info = []

    for user in users:
        role = user.role.name if user.role else 'No Role'
        groups = user.groups.all()
        group_names = ', '.join(group.name for group in groups)
        permissions = Permission.objects.filter(group__user=user).distinct()
        permission_codenames = ', '.join(permission.codename for permission in permissions)
        user_permissions_info.append(
            f"User: {user.username}, Role: {role}, Groups: {group_names}, Permissions: {permission_codenames}"
        )

    return user_permissions_info


# Example of usage
for info in get_user_permissions():
    print(info)
