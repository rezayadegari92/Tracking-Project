
from django.db.models.signals import post_save
from django.dispatch import receiver
from  django.contrib.auth.models import Group

from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def assign_user_group(sender, instance, created, **kwargs):
    if created:
        if instance.user_type() == "partner":
            group, _ = Group.objects.get_or_create(name="Partners")
            instance.groups.add(group)
        elif instance.user_type == "Customer":
            group, _ = Group.objects.get_or_create(name="Customers")
            instance.groups.add(group)
