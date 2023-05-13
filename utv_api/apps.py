from django.apps import AppConfig
from django.core.signals import request_finished


class UtvApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'utv_api'
    verbose_name = "API"

    def ready(self):
        from utv_api.signals import post_save_comments
        request_finished.connect(post_save_comments)
