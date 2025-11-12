from django.apps import AppConfig


class ArchitectsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # Use the full Python path to the app package so Django can import it correctly
    name = 'app.architects'
