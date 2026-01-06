# core/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Subscriber


@receiver(post_save, sender=Subscriber)
def subscriber_created(sender, instance, created, **kwargs):
    if created:
        # future: analytics, logging, onboarding workflows
        print(f"New subscriber: {instance.email}")

