# Em config/urls.py (ARQUIVO COMPLETO E CORRIGIDO)

from django.contrib import admin
from django.urls import path, include

# Imports das views de 'usuarios'
from usuarios.views import CadastroView, HomeView, MinhasApostasView

# Imports das views de 'apostas' (COM A VIEW DE CASHOUT)
from apostas.views import FazerApostaView, CashoutApostaView 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # URLs de Usuário
    path('contas/', include('django.contrib.auth.urls')), 
    path('cadastro/', CadastroView.as_view(), name='cadastro'),
    path('', HomeView.as_view(), name='home'),
    path('minhas-apostas/', MinhasApostasView.as_view(), name='minhas_apostas'),
    
    # URLs de Aposta
    path('jogo/<int:pk>/', FazerApostaView.as_view(), name='fazer_aposta'),
    
    # URL DE CASHOUT (A LINHA QUE FALTAVA)
    path('cashout/<int:pk>/', CashoutApostaView.as_view(), name='cashout_aposta'),
]