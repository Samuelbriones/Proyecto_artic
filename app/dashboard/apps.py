from django.apps import AppConfig


class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # Use full dotted path consistent with project structure
    name = 'app.dashboard'
