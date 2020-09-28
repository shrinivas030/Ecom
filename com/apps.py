from django.apps import AppConfig


class ComConfig(AppConfig):
    name = 'com'

    def ready(self):
        import com.signals