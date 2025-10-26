# Em apostas/forms.py (ARQUIVO CORRIGIDO DE INDENTAÇÃO)

from django import forms
from .models import Aposta

class ApostaForm(forms.ModelForm):
    
    # Vamos declarar o campo 'escolha' aqui, mas sem as 'choices'
    escolha = forms.ChoiceField(
        widget=forms.RadioSelect # Mostra como botões de rádio
    )
    
    # O ERRO ESTAVA AQUI: Esta classe estava indentada
    # Agora está correta:
    class Meta:
        model = Aposta
        # Campos que o usuário vai preencher
        fields = ['valor_apostado', 'escolha']
        
        widgets = {
            'valor_apostado': forms.NumberInput(attrs={
                'min': '1.00',
                # HINTS PARA O NAVEGADOR MOBILE:
                'inputmode': 'decimal', # Pede o numpad com decimal
                'pattern': '[0-9.,]*'   # Regra do que é permitido
            }),
        }

    # ESTA FUNÇÃO FOI MODIFICADA
    def __init__(self, *args, **kwargs):
        # 1. Pegamos o 'usuario' e o 'jogo' que a View nos mandou
        self.usuario = kwargs.pop('usuario', None)
        self.jogo = kwargs.pop('jogo', None)
        
        # 2. Chamamos o 'super' (inicializador padrão)
        super().__init__(*args, **kwargs)

        # 3. ESTA É A MÁGICA:
        # Se nós recebemos um 'jogo' (o que sempre acontece)...
        if self.jogo:
            # ...nós definimos as 'choices' do campo 'escolha' DINAMICAMENTE
            self.fields['escolha'].choices = [
                ('TIME_A', f'Vitória: {self.jogo.time_a}'), # Ex: 'Vitória: Corinthians'
                ('TIME_B', f'Vitória: {self.jogo.time_b}'), # Ex: 'Vitória: Flamengo'
                ('EMPATE', 'Empate'),
            ]

    #
    # O RESTO DO ARQUIVO (AS VALIDAÇÕES) CONTINUA IGUAL
    #
    def clean_valor_apostado(self):
        valor = self.cleaned_data.get('valor_apostado')
        
        if self.usuario and valor > self.usuario.saldo:
            raise forms.ValidationError('Você não tem saldo suficiente para esta aposta.')
        
        if valor <= 0:
            raise forms.ValidationError('O valor da aposta deve ser positivo.')
            
        return valor
        
    def clean(self):
        cleaned_data = super().clean()
        
        if self.jogo and self.jogo.status != 'ABERTO':
            raise forms.ValidationError('Este jogo não está mais aberto para apostas.')

        if self.usuario and self.jogo:
            if Aposta.objects.filter(
                usuario=self.usuario, 
                jogo=self.jogo, 
                status='PENDENTE'
            ).exists():
                raise forms.ValidationError('Você já tem uma aposta PENDENTE neste jogo.')
        
        return cleaned_data