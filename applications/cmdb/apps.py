from django.apps import AppConfig


class CmdbConfig(AppConfig):
    name = 'cmdb'

    def ready(self):
        print("ready")
        import receivers
