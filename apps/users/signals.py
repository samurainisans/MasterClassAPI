# C:/Users/Nik/Desktop/DjangoBackendMasterclases/MasterClassAPI/apps/users/signals.py
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import User


@receiver(pre_save, sender=User)
def pre_save_assign_user_to_group(sender, instance, **kwargs):
    if not instance.pk:
        # User is being created, no need to check the old role
        return
    try:
        old_instance = User.objects.get(pk=instance.pk)
    except User.DoesNotExist:
        # User does not exist, no old role to compare
        return

    if old_instance.role != instance.role:
        if instance.role:
            group, created = Group.objects.get_or_create(name=instance.role.name)
            instance.groups.set([group])


@receiver(post_save, sender=User)
def post_save_assign_user_to_group(sender, instance, created, **kwargs):
    if created:
        if instance.role:
            group, created = Group.objects.get_or_create(name=instance.role.name)
            instance.groups.set([group])
