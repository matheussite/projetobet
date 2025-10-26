from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UsuarioCustomizado

# Este form será usado na página de CADASTRO
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UsuarioCustomizado
        # Quais campos devem aparecer no cadastro
        fields = ('username', 'email')

# Este form será usado no Admin (opcional, mas bom ter)
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = UsuarioCustomizado
        fields = ('username', 'email')