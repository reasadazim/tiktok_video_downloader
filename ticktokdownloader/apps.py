from django.apps import AppConfig


class TicktokdownloaderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ticktokdownloader'

    def ready(self):
        from .jobs import updater
        updater.start()
