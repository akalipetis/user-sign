from django.apps import AppConfig


class SignaturesConfig(AppConfig):
    name = 'signatures'

    def ready(self):
        from signatures import signals
