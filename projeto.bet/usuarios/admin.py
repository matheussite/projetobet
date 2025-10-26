from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UsuarioCustomizado

# Vamos customizar como o admin do Django lida com nosso usuário
class CustomUserAdmin(UserAdmin):
    model = UsuarioCustomizado
    
    # Quais colunas devem aparecer na lista de usuários
    list_display = ['username', 'email', 'saldo', 'is_staff']
    
    # Quais campos aparecem ao *editar* um usuário
    # (Estamos adicionando 'saldo' aos campos que o UserAdmin já tem)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('saldo',)}),
    )
    
    # Quais campos aparecem ao *criar* um novo usuário no admin
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('saldo',)}),
    )

# Diz ao site de admin para usar nossa classe 'CustomUserAdmin'
# para o modelo 'UsuarioCustomizado'
admin.site.register(UsuarioCustomizado, CustomUserAdmin)