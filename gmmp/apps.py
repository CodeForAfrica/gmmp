from django.apps import AppConfig

class GmmpConfig(AppConfig):
    name = 'gmmp'

    def ready(self):
        import gmmp.signals 