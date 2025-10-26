from django.db import models
from django.contrib.auth.models import AbstractUser

# Vamos criar nossa própria classe de usuário,
# herdando (pegando tudo) do usuário padrão do Django (AbstractUser)
class UsuarioCustomizado(AbstractUser):
    
    # O AbstractUser já tem:
    # username, password, email, first_name, last_name, etc.
    
    # Agora, adicionamos nosso campo extra:
    saldo = models.DecimalField(
        max_digits=10,       # Quantidade máxima de dígitos (ex: 12345678,99)
        decimal_places=2,  # Quantidade de casas decimais
        default=1000.00    # Saldo inicial que o usuário ganha ao se cadastrar
    )

    # Isso ajuda a mostrar um nome legível no painel de admin
    def __str__(self):
        return self.username