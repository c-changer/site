from django.apps import AppConfig


class CryptoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crypto'
    
    verbose_name = "Сервис"
    
    def ready(self):
        import crypto.signals
