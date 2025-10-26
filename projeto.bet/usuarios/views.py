# Em usuarios/views.py (O CÓDIGO CORRETO)

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin 
from apostas.models import Jogo, Aposta
# O IMPORT CORRETO (precisamos do form de CADASTRO):
from .forms import CustomUserCreationForm 

#
# CLASSE 1: CADASTRO
#
class CadastroView(CreateView):
  form_class = CustomUserCreationForm # <-- Agora isso funciona
  success_url = reverse_lazy('login') 
  template_name = 'cadastro.html'

#
# CLASSE 2: HOME
#
class HomeView(LoginRequiredMixin, ListView):
    model = Jogo
    template_name = "home.html"
    context_object_name = "lista_jogos"
    login_url = 'login'

    def get_queryset(self):
        return Jogo.objects.filter(status='ABERTO').order_by('data_jogo')

#
# CLASSE 3: MINHAS APOSTAS
#
class MinhasApostasView(LoginRequiredMixin, ListView):
    model = Aposta
    template_name = 'minhas_apostas.html'
    context_object_name = 'minhas_apostas'
    login_url = 'login'

    def get_queryset(self):
        return Aposta.objects.filter(
            usuario=self.request.user
        ).select_related('jogo').order_by('-data_aposta')