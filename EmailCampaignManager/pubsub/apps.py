from django.apps import AppConfig


class PubsubConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pubsub"

    def ready(self):
        import pubsub.signals  # Import your signals module

        # Register the 'post_migrate' signal to call 'on_startup'
        from django.db.models.signals import post_migrate
        from .subscriber import subscribe_to_email_campaigns
        from django.dispatch import receiver
        @receiver(post_migrate, sender=self)
        def on_startup(sender, **kwargs):
            subscribe_to_email_campaigns()


