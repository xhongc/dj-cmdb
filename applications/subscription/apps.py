from django.apps import AppConfig


class SubscriptionConfig(AppConfig):
    name = 'applications.subscription'

    def ready(self):
        print("ready")
        from . import receivers
