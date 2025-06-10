# Create your models here.
from django.db import models
from django.conf import settings
import os

# Opções de imagens padrão
OPCOES_IMAGEM_PADRAO = [
    ('capa-ceia', 'Culto de Ceia'),
    ('capa-divino', 'Culto Divino'),
    ('capa-ebd', 'EBD'),
    ('capa-maravilhas', 'Culto das Maravilhas'),
    ('capa-louvor', 'Culto de Louvor'),
    ('personalizada', 'Imagem Personalizada (Upload)'),
]

class ConfiguracaoSite(models.Model):
    link_youtube = models.URLField(
        max_length=255, 
        verbose_name="Link do YouTube",
        help_text="URL do vídeo do YouTube que será exibido na página principal"
    )
    titulo_video = models.CharField(
        max_length=100, 
        verbose_name="Título do Vídeo",
        help_text="Título que será exibido acima do vídeo",
        default="Última Transmissão ao Vivo"
    )
    tipo_imagem = models.CharField(
        max_length=20,
        choices=OPCOES_IMAGEM_PADRAO,
        default='capa-maravilhas',
        verbose_name="Tipo de Imagem",
        help_text="Selecione uma imagem padrão ou escolha 'Imagem Personalizada' para fazer upload"
    )
    imagem_personalizada = models.ImageField(
        upload_to='uploads/capas/',
        blank=True,
        null=True,
        verbose_name="Imagem Personalizada",
        help_text="Faça upload de uma imagem personalizada (apenas se 'Tipo de Imagem' for 'Imagem Personalizada')"
    )
    data_atualizacao = models.DateTimeField(
        auto_now=True, 
        verbose_name="Data de Atualização"
    )

    class Meta:
        verbose_name = "Configuração do Site"
        verbose_name_plural = "Configurações do Site"

    def __str__(self):
        return f"Configurações do Site - Atualizado em {self.data_atualizacao.strftime('%d/%m/%Y %H:%M')}"

    def save(self, *args, **kwargs):
        # Garantir que só exista uma instância deste modelo
        if ConfiguracaoSite.objects.exists() and not self.pk:
            # Se já existe uma configuração e estamos tentando criar outra,
            # atualizamos a existente em vez de criar uma nova
            raise ValueError("Já existe uma configuração. Edite a existente em vez de criar uma nova.")
        
        # Se o tipo de imagem não for personalizada, limpar o campo de imagem personalizada
        if self.tipo_imagem != 'personalizada':
            # Se havia uma imagem personalizada antes, podemos excluí-la para economizar espaço
            if self.pk:
                old_instance = ConfiguracaoSite.objects.get(pk=self.pk)
                if old_instance.imagem_personalizada and old_instance.tipo_imagem == 'personalizada':
                    if os.path.isfile(old_instance.imagem_personalizada.path):
                        os.remove(old_instance.imagem_personalizada.path)
            self.imagem_personalizada = None
            
        return super().save(*args, **kwargs)
    
    def get_imagem_url(self):
        """Retorna a URL da imagem a ser exibida, seja padrão ou personalizada"""
        if self.tipo_imagem == 'personalizada' and self.imagem_personalizada:
            return self.imagem_personalizada.url
        else:
            # Retorna o caminho para a imagem padrão
            return f"{settings.STATIC_URL}fotos/{self.tipo_imagem}.jpeg"


# --- NOVO MODELO APENAS PARA DEPARTAMENTOS --- 
class Departamento(models.Model):
    CATEGORIAS = [
        ("TREINAMENTO", "Ministério de Treinamento e Crescimento Cristão"),
        ("MUSICA", "Ministério de Música"),
        # Adicione mais categorias se necessário no futuro
    ]

    nome = models.CharField(max_length=100, verbose_name="Nome do Departamento")
    descricao = models.TextField(blank=True, help_text="Uma breve descrição do departamento.", verbose_name="Descrição")
    imagem = models.ImageField(upload_to="departamentos/", help_text="Imagem representativa do departamento.", verbose_name="Imagem")
    categoria = models.CharField(max_length=50, choices=CATEGORIAS, verbose_name="Ministério Principal")
    ordem = models.PositiveIntegerField(default=0, help_text="Define a ordem de exibição dentro do ministério (menor número aparece primeiro).", verbose_name="Ordem de Exibição")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
        ordering = ["categoria", "ordem"] # Ordena por ministério e depois pela ordem definida

# --- ADIÇÕES NO MODELO PARA LIDERANÇA ---
class SecaoLideranca(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título da Seção")
    descricao = models.TextField(blank=True, verbose_name="Texto de Descrição")
    ordem = models.PositiveIntegerField(default=0, help_text="Define a ordem de exibição na página (menor número aparece primeiro).")

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Seção de Liderança"
        verbose_name_plural = "Seções de Liderança"
        ordering = ['ordem']


class Pessoa(models.Model):
    secao = models.ForeignKey(SecaoLideranca, on_delete=models.CASCADE, related_name='pessoas')
    nome = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100, verbose_name="Cargo ou Função")
    descricao = models.TextField(blank=True, verbose_name="Descrição")
    foto = models.ImageField(upload_to='lideranca/', verbose_name="Foto")
    ordem = models.PositiveIntegerField(default=0, help_text="Define a ordem de exibição dentro da seção.")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Pessoa da Liderança"
        verbose_name_plural = "Pessoas da Liderança"
        ordering = ['ordem']