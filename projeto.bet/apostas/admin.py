from django.contrib import admin
from .models import Jogo, Aposta

# Para mostrar os jogos de forma mais amigável no admin
class JogoAdmin(admin.ModelAdmin):
    list_display = ('time_a', 'time_b', 'data_jogo', 'status', 'resultado')
    # Adiciona filtros fáceis na lateral
    list_filter = ('status', 'data_jogo')

# Para mostrar as apostas de forma mais amigável
class ApostaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'jogo', 'valor_apostado', 'escolha', 'status')
    list_filter = ('status', 'usuario', 'jogo')

# Registra os modelos no site de admin
admin.site.register(Jogo, JogoAdmin)
admin.site.register(Aposta, ApostaAdmin)