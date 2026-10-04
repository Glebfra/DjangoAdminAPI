from django.apps import AppConfig

class AdminApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"

    name = "admin_api"
    
    verbose_name = "Django Admin API"

    def ready(self) -> None:
        from .autodiscover import autodiscover
        
        autodiscover()
