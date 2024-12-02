from django.apps import AppConfig


class UserAndEmailManagerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.user_and_email_manager"
    verbose_name = "Управление рассылками пользователям"
