from django.apps import AppConfig


class ReportsConfig(AppConfig):
    name = "reports"

    def ready(self):
        import reports.signals
