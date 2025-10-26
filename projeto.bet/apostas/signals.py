from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Jogo
from .models import processar_apostas_finalizadas # Importa nossa função

# Este "decorator" diz: "quando um Jogo for salvo (post_save), 
# chame esta função"
@receiver(post_save, sender=Jogo)
def ao_salvar_jogo(sender, instance, created, **kwargs):
    """
    Processa as apostas quando um Jogo é salvo com status FINALIZADO.
    'instance' é o objeto Jogo que acabou de ser salvo.
    """
    print(f"Sinal recebido para Jogo ID: {instance.id}, Status: {instance.status}")

    # Verificamos se o status é FINALIZADO
    if instance.status == 'FINALIZADO':
        # Chamamos nossa função de processamento
        processar_apostas_finalizadas(instance.id)