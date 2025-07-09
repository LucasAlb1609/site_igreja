from django.contrib import admin
from django.utils.html import format_html
from .models import ConfiguracaoSite, Departamento, SecaoLideranca, Pessoa, DiaSemana, Evento, EventoEspecial, Devocional

class ConfiguracaoSiteAdmin(admin.ModelAdmin):
    list_display = ('titulo_video', 'link_youtube', 'tipo_imagem', 'preview_imagem', 'data_atualizacao')
    readonly_fields = ('data_atualizacao', 'preview_imagem')
    fieldsets = (
        ('Configurações do Vídeo', {
            'fields': ('titulo_video', 'link_youtube')
        }),
        ('Configurações da Imagem', {
            'fields': ('tipo_imagem', 'imagem_personalizada', 'preview_imagem'),
            'description': 'Selecione uma imagem padrão ou faça upload de uma imagem personalizada.'
        }),
        ('Informações do Sistema', {
            'fields': ('data_atualizacao',),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        # Verifica se já existe uma configuração
        return not ConfiguracaoSite.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Impede a exclusão da configuração
        return False
    
    def preview_imagem(self, obj):
        """Exibe uma prévia da imagem selecionada"""
        if obj.pk:  # Verifica se o objeto já foi salvo
            return format_html('<img src="{}" style="max-height: 150px; max-width: 300px;" />', obj.get_imagem_url())
        return "Salve para visualizar a prévia da imagem"
    preview_imagem.short_description = "Prévia da Imagem"

admin.site.register(ConfiguracaoSite, ConfiguracaoSiteAdmin)

# --- ADMIN PARA DEVOCIONAIS ---
@admin.register(Devocional)
class DevocionalAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'data_publicacao')
    list_filter = ('autor', 'data_publicacao')
    search_fields = ('titulo', 'conteudo')
    fieldsets = (
        (None, {
            'fields': ('titulo', 'subtitulo', 'autor', 'data_publicacao')
        }),
        ('Mídia e Conteúdo', {
            'fields': ('imagem', 'conteudo')
        }),
    )

# --- NOVO ADMIN APENAS PARA DEPARTAMENTOS --- 
@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ("nome", "categoria", "ordem", "imagem_preview")
    list_filter = ("categoria",)
    search_fields = ("nome", "descricao")
    list_editable = ("ordem",)
    
    fieldsets = (
        (None, {
            "fields": ("nome", "categoria", "ordem")
        }),
        ("Conteúdo", {
            "fields": ("descricao", "imagem")
        }),
    )

    def imagem_preview(self, obj):
        if obj.imagem:
            # Garante que a URL da imagem seja acessível
            try:
                url = obj.imagem.url
                return format_html("<img src=\"{}\" width=\"100\" />", url)
            except ValueError:
                return "(Erro ao carregar imagem)"
        return "(Sem imagem)"
    imagem_preview.short_description = "Prévia da Imagem"


# Permite editar Pessoas dentro da página da Seção
class PessoaInline(admin.TabularInline):
    model = Pessoa
    extra = 1  # Quantos formulários em branco exibir
    fields = ('nome', 'cargo', 'descricao', 'foto', 'ordem')


@admin.register(SecaoLideranca)
class SecaoLiderancaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ordem')
    list_editable = ('ordem',)
    inlines = [PessoaInline]


class EventoInline(admin.TabularInline):
    model = Evento
    extra = 1

@admin.register(DiaSemana)
class DiaSemanaAdmin(admin.ModelAdmin):
    list_display = ('get_nome_display', 'resumo')
    inlines = [EventoInline]

    def get_nome_display(self, obj):
        return obj.get_nome_display()
    get_nome_display.short_description = 'Dia da Semana'
    get_nome_display.admin_order_field = 'nome'


@admin.register(EventoEspecial)
class EventoEspecialAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'periodo', 'ordem')
    list_editable = ('ordem',)