from django.apps import AppConfig


class PasswordlessLoginConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "passwordless_login"

    def ready(self):
        from . import settings
