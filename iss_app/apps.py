from django.apps import AppConfig


class IssAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "iss_app"

    def ready(self):
        from background_tasks import updater
        updater.check_loc()
