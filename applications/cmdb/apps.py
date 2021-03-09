from django.apps import AppConfig


class CmdbConfig(AppConfig):
    name = 'applications.cmdb'

    def ready(self):
        print("ready")
        from . import receivers
