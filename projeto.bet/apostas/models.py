from django.db import models
# Vamos importar o nosso usuário customizado
from usuarios.models import UsuarioCustomizado

from decimal import Decimal

class Jogo(models.Model):
    # Opções de status do jogo
    STATUS_CHOICES = (
        ('ABERTO', 'Aberto para apostas'),
        ('FINALIZADO', 'Finalizado'),
        ('CANCELADO', 'Cancelado'),
    )

    # Opções de resultado
    RESULTADO_CHOICES = (
        ('TIME_A', 'Vitória Time A'),
        ('TIME_B', 'Vitória Time B'),
        ('EMPATE', 'Empate'),
    )

    time_a = models.CharField(max_length=100)
    time_b = models.CharField(max_length=100)

    # Odds (quanto paga)
    odd_time_a = models.DecimalField(max_digits=5, decimal_places=2)
    odd_time_b = models.DecimalField(max_digits=5, decimal_places=2)
    odd_empate = models.DecimalField(max_digits=5, decimal_places=2)

    data_jogo = models.DateTimeField()

    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='ABERTO'
    )

    # O resultado só será preenchido pelo admin
    resultado = models.CharField(
        max_length=20, 
        choices=RESULTADO_CHOICES, 
        null=True, # Pode ser nulo (jogo ainda não acabou)
        blank=True # Pode ser em branco no admin
    )

    def __str__(self):
        # Isso é o que vai aparecer no Admin (ex: "Time A vs Time B")
        return f"{self.time_a} vs {self.time_b}"


class Aposta(models.Model):
    # Opções de escolha do usuário
    ESCOLHA_CHOICES = (
        ('TIME_A', 'Vitória Time A'),
        ('TIME_B', 'Vitória Time B'),
        ('EMPATE', 'Empate'),
    )

    # Status da aposta
    STATUS_APOSTA_CHOICES = (
        ('PENDENTE', 'Pendente'),
        ('GANHA', 'Ganha'),
        ('PERDIDA', 'Perdida'),
        ('CASHED_OUT', 'Cashout Realizado'), # <-- ADICIONE ESTA LINHA
    )

    # RELACIONAMENTOS
    # related_name='apostas' permite fazer usuario.apostas.all()
    usuario = models.ForeignKey(
        UsuarioCustomizado, 
        on_delete=models.CASCADE, 
        related_name='apostas'
    )

    jogo = models.ForeignKey(
        Jogo, 
        on_delete=models.CASCADE, 
        related_name='apostas'
    )

    # VALORES
    valor_apostado = models.DecimalField(max_digits=10, decimal_places=2)

    escolha = models.CharField(max_length=20, choices=ESCOLHA_CHOICES)

    status = models.CharField(
        max_length=20, 
        choices=STATUS_APOSTA_CHOICES, 
        default='PENDENTE'
    )

    data_aposta = models.DateTimeField(auto_now_add=True) # Salva a data agora

    def __str__(self):
        return f"Aposta de {self.usuario.username} em {self.jogo}"
    
    from decimal import Decimal

# Esta é a função que vai processar os pagamentos
def processar_apostas_finalizadas(jogo_id):
    try:
        jogo = Jogo.objects.get(id=jogo_id)
    except Jogo.DoesNotExist:
        return # Jogo não existe

    # Só processa se o jogo estiver "Finalizado" e tiver um "Resultado"
    if jogo.status != 'FINALIZADO' or not jogo.resultado:
        return

    # Busca todas as apostas PENDENTES para este jogo
    apostas_pendentes = Aposta.objects.filter(jogo=jogo, status='PENDENTE')

    for aposta in apostas_pendentes:
        usuario = aposta.usuario

        # 1. Verifica se o usuário GANHOU
        if aposta.escolha == jogo.resultado:
            # Pega a Odd correta
            odd_ganha = Decimal('0.00') # Inicia com 0
            if jogo.resultado == 'TIME_A':
                odd_ganha = jogo.odd_time_a
            elif jogo.resultado == 'TIME_B':
                odd_ganha = jogo.odd_time_b
            elif jogo.resultado == 'EMPATE':
                odd_ganha = jogo.odd_empate

            # Calcula o prêmio
            premio = aposta.valor_apostado * odd_ganha

            # Paga o usuário
            usuario.saldo += premio
            usuario.save()

            # Atualiza a aposta
            aposta.status = 'GANHA'

        # 2. Se não ganhou, ele PERDEU
        else:
            aposta.status = 'PERDIDA'

        # Salva o novo status da aposta
        aposta.save()

    print(f"Apostas para o jogo {jogo.id} processadas.")