from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .subscriber import subscribe_to_email_campaigns

# on startup of app, subscribing to redis_channel and listening to it
@receiver(post_migrate, sender=AppConfig)
def on_startup(sender, **kwargs):
    print("Subscribe Function called")
    subscribe_to_email_campaigns()
