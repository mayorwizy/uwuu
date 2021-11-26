from django.db.models.signals import post_save
from .models import UserProfile, Account
#import User this is the default django user model import
# from django.contrib.auth.models 
from django . dispatch import receiver


@receiver(post_save, sender=Account)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


# post_save.connect(create_profile, sender=User)


@receiver(post_save, sender=Account)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
