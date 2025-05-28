from django.contrib import admin
from django.utils.html import format_html
from .models import ConfiguracaoSite

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
