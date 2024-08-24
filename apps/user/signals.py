from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .utils import send_verification_code

User = get_user_model()


@receiver(post_save, sender=User)
def send_code_on_user_creation(sender, instance, created, **kwargs):
    if created:
        send_verification_code(instance)
