# Em apostas/views.py (O CÓDIGO CORRETO)

# Imports que JÁ ESTAVAM no seu arquivo
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Jogo, Aposta
from .forms import ApostaForm # <-- Este arquivo SIM precisa do ApostaForm
from decimal import Decimal
from django.http import HttpResponseForbidden

# ===== IMPORTS NOVOS (Para o Hack do Admin) =====
from django.http import HttpResponse
from django.contrib.auth import get_user_model
# ===============================================


#
# CLASSE 1: FAZER APOSTA (Seu código - INTACTO)
#
class FazerApostaView(LoginRequiredMixin, View):
    login_url = '/contas/login/'
    
    def get(self, request, pk):
        jogo = get_object_or_404(Jogo, pk=pk)
        form = ApostaForm(usuario=request.user, jogo=jogo)
        return render(request, 'jogo_detalhe.html', {'jogo': jogo, 'form': form})

    def post(self, request, pk):
        jogo = get_object_or_404(Jogo, pk=pk)
        form = ApostaForm(request.POST, usuario=request.user, jogo=jogo)
        
        if form.is_valid():
            valor = form.cleaned_data['valor_apostado']
            usuario = request.user
            usuario.saldo -= valor
            usuario.save()
            
            aposta = form.save(commit=False)
            aposta.usuario = usuario
            aposta.jogo = jogo
            aposta.save()
            
            messages.success(request, 'Aposta realizada com sucesso!')
            return redirect('home')
        
        return render(request, 'jogo_detalhe.html', {'jogo': jogo, 'form': form})

#
# CLASSE 2: CASHOUT (Seu código - INTACTO)
#
class CashoutApostaView(LoginRequiredMixin, View):
    login_url = '/contas/login/'

    def post(self, request, pk):
        aposta = get_object_or_404(Aposta, pk=pk)

        if aposta.usuario != request.user:
            return HttpResponseForbidden("Você não tem permissão para esta ação.")

        if aposta.status == 'PENDENTE' and aposta.jogo.status == 'ABERTO':
            valor_apostado = aposta.valor_apostado
            valor_cashout = valor_apostado * Decimal('0.80') 
            
            usuario = request.user
            usuario.saldo += valor_cashout
            usuario.save()
            
            aposta.status = 'CASHED_OUT'
            aposta.save()
            
            messages.success(request, f'Cashout de R$ {valor_cashout:.2f} realizado com sucesso!')
        
        else:
            messages.error(request, 'Não é possível fazer cashout desta aposta.')

        return redirect('minhas_apostas')

#
# ===== CÓDIGO NOVO (Hack do Admin) =====
# Cole esta função no FINAL do arquivo
# ========================================
def criar_admin_temporario(request):
    User = get_user_model()
    username = 'admin' # <--- Seu login
    password = 'admin123' # <--- Sua senha temporária
    
    if not User.objects.filter(username=username).exists():
        print("Criando superusuário...") # Mensagem para o log
        User.objects.create_superuser(username=username, password=password, email='admin@email.com')
        print("Superusuário criado.")
        return HttpResponse("<h1>Admin criado!</h1><p>Usuário: 'admin', Senha: 'admin123'. Agora pode ir para /admin e logar. <strong>APAGUE ESSE CÓDIGO AGORA!</strong></p>")
    else:
        print("Superusuário já existe.")
        return HttpResponse("<h1>Admin já existe.</h1> <a href='/admin/'>Ir para o Admin</a>")