# usuarios/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Filho

class FilhoInline(admin.TabularInline):
    """
    Permite a edição dos filhos diretamente na página do usuário.
    """
    model = Filho
    extra = 1  # Mostra um campo extra para adicionar um novo filho
    fields = ('nome_completo', 'data_nascimento')


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Configuração do painel administrativo para o modelo de usuário personalizado.
    """
    inlines = [FilhoInline]

    # Campos exibidos na lista de usuários
    list_display = (
        'username', 'nome_completo', 'email', 'papel', 
        'aprovado', 'ativo', 'cpf', 'telefone', 'data_cadastro'
    )
    
    # Filtros laterais
    list_filter = (
        'papel', 'aprovado', 'ativo', 'estado_civil', 'batizado_aguas',
        'membro_congregacao', 'frequenta_escola_biblica', 'data_cadastro'
    )
    
    # Campos de busca
    search_fields = ('username', 'nome_completo', 'email', 'telefone', 'cpf', 'rg')
    
    # Ordenação padrão
    ordering = ('nome_completo',)
    
    # Configuração dos fieldsets para o formulário de edição
    fieldsets = (
        ('Informações de Login', {
            'fields': ('username', 'password')
        }),
        ('Status no Sistema', {
            'fields': ('papel', 'ativo', 'aprovado', 'aprovado_por', 'data_aprovacao')
        }),
        ('Informações Pessoais', {
            'fields': (
                'nome_completo', 'email', 'foto_perfil', 'data_nascimento', 'cpf', 'rg',
                'naturalidade', 'nome_pai', 'nome_mae', 'telefone',
                'estado_civil', 'nome_conjuge', 'data_casamento',
                'tem_alergia_medicacao', 'alergias_texto'
            )
        }),
        ('Endereço', {
            'fields': ('endereco', 'bairro', 'cidade', 'cep'),
            'classes': ('collapse',)
        }),
        ('Profissão e Educação', {
            'fields': ('profissao', 'nivel_escolar'),
            'classes': ('collapse',)
        }),
        ('Informações Eclesiásticas', {
            'fields': (
                'data_conversao', 'batizado_aguas', 'data_batismo', 'local_batismo',
                'outra_igreja_batismo', 'recebido_por_aclamacao',
                'membro_congregacao', 'qual_congregacao',
                'frequenta_escola_biblica', 'qual_classe_escola_biblica',
                'deseja_exercer_funcao', 'qual_funcao_deseja'
            )
        }),
        ('Permissões do Django', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Datas Importantes', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    
    # Campos para o formulário de criação de usuário no admin
    add_fieldsets = (
        ('Informações Básicas', {
            'classes': ('wide',),
            'fields': ('username', 'nome_completo', 'email', 'password', 'password2'),
        }),
        ('Sistema', {
            'fields': ('papel', 'ativo', 'aprovado')
        }),
    )
    
    # Ações personalizadas
    actions = ['aprovar_usuarios', 'desaprovar_usuarios', 'ativar_usuarios', 'desativar_usuarios']
    
    def aprovar_usuarios(self, request, queryset):
        """Aprovar usuários selecionados"""
        from django.utils import timezone
        updated = queryset.update(
            aprovado=True, 
            aprovado_por=request.user, 
            data_aprovacao=timezone.now()
        )
        self.message_user(request, f'{updated} usuário(s) aprovado(s) com sucesso.')
    aprovar_usuarios.short_description = "Aprovar usuários selecionados"
    
    def desaprovar_usuarios(self, request, queryset):
        """Desaprovar usuários selecionados"""
        updated = queryset.update(
            aprovado=False, 
            aprovado_por=None, 
            data_aprovacao=None
        )
        self.message_user(request, f'{updated} usuário(s) desaprovado(s) com sucesso.')
    desaprovar_usuarios.short_description = "Desaprovar usuários selecionados"
    
    def ativar_usuarios(self, request, queryset):
        """Ativar usuários selecionados"""
        updated = queryset.update(ativo=True)
        self.message_user(request, f'{updated} usuário(s) ativado(s) com sucesso.')
    ativar_usuarios.short_description = "Ativar usuários selecionados"
    
    def desativar_usuarios(self, request, queryset):
        """Desativar usuários selecionados"""
        updated = queryset.update(ativo=False)
        self.message_user(request, f'{updated} usuário(s) desativado(s) com sucesso.')
    desativar_usuarios.short_description = "Desativar usuários selecionados"