from django.apps import AppConfig

class ApostasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apostas'

    # ADICIONE ESTA FUNÇÃO:
    def ready(self):
        import apostas.signals # Importa nossos sinais