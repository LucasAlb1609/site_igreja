# usuarios/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

class User(AbstractUser):
    """
    Modelo de usuário personalizado baseado na ficha de cadastro da igreja.
    """
    
    # --- DADOS DE LOGIN (herdado) ---
    # username, password, email, first_name, last_name
    
    # --- DADOS PESSOAIS ---
    nome_completo = models.CharField(max_length=200, verbose_name="Nome Completo")
    
    foto_perfil = models.ImageField(
        upload_to='perfil_fotos/', 
        verbose_name="Foto do Perfil", 
        null=True, 
        blank=True
    )
    
    data_nascimento = models.DateField(verbose_name="Data de Nascimento", null=True, blank=True)
    
    nome_pai = models.CharField(max_length=200, verbose_name="Nome do Pai", blank=True)
    nome_mae = models.CharField(max_length=200, verbose_name="Nome da Mãe", blank=True)
    
    cpf_validator = RegexValidator(
        regex=r'^\d{11}$',
        message="CPF deve conter 11 dígitos, sem pontos ou traços."
    )
    cpf = models.CharField(
        max_length=11, 
        validators=[cpf_validator], 
        verbose_name="CPF", 
        unique=True, 
        null=True, 
        blank=True
    )
    
    rg = models.CharField(max_length=20, verbose_name="RG", blank=True)
    naturalidade = models.CharField(max_length=150, verbose_name="Natural da cidade de", blank=True)

    ESTADO_CIVIL_CHOICES = [
        ('solteiro', 'Solteiro(a)'),
        ('casado', 'Casado(a)'),
        ('divorciado', 'Divorciado(a)'),
        ('viuvo', 'Viúvo(a)'),
    ]
    estado_civil = models.CharField(
        max_length=20, 
        choices=ESTADO_CIVIL_CHOICES, 
        verbose_name="Estado Civil",
        blank=True
    )
    
    nome_conjuge = models.CharField(max_length=200, verbose_name="Nome do Cônjuge", blank=True)
    data_casamento = models.DateField(verbose_name="Data de Casamento", null=True, blank=True)

    tem_alergia_medicacao = models.BooleanField(default=False, verbose_name="Possui alergia a alguma medicação?")
    alergias_texto = models.TextField(verbose_name="Quais alergias?", blank=True)
    
    # --- CONTATO ---
    telefone_validator = RegexValidator(
        regex=r'^\(\d{2}\)\s\d{4,5}-\d{4}$',
        message="Telefone deve estar no formato: (XX) XXXX-XXXX ou (XX) XXXXX-XXXX"
    )
    telefone = models.CharField(
        max_length=15, 
        validators=[telefone_validator], 
        verbose_name="Telefone",
        blank=True
    )
    
    # --- ENDEREÇO ---
    endereco = models.CharField(max_length=300, verbose_name="Endereço", blank=True)
    bairro = models.CharField(max_length=100, verbose_name="Bairro", blank=True)
    cidade = models.CharField(max_length=100, verbose_name="Cidade", blank=True)
    cep = models.CharField(max_length=10, verbose_name="CEP", blank=True)
    
    # --- PROFISSÃO E EDUCAÇÃO ---
    profissao = models.CharField(max_length=150, verbose_name="Profissão", blank=True)
    
    NIVEL_ESCOLAR_CHOICES = [
        ('fundamental_incompleto', 'Ensino Fundamental Incompleto'),
        ('fundamental_completo', 'Ensino Fundamental Completo'),
        ('medio_incompleto', 'Ensino Médio Incompleto'),
        ('medio_completo', 'Ensino Médio Completo'),
        ('superior_incompleto', 'Ensino Superior Incompleto'),
        ('superior_completo', 'Ensino Superior Completo'),
        ('pos_graduacao', 'Pós-graduação'),
        ('nao_informar', 'Não desejo informar'),
    ]
    nivel_escolar = models.CharField(
        max_length=30, 
        choices=NIVEL_ESCOLAR_CHOICES, 
        verbose_name="Nível Escolar",
        blank=True
    )
    
    # --- INFORMAÇÕES ECLESIÁSTICAS ---
    data_conversao = models.DateField(verbose_name="Data de Conversão", null=True, blank=True)
    
    batizado_aguas = models.BooleanField(default=False, verbose_name="É batizado nas águas?")
    data_batismo = models.DateField(verbose_name="Data do Batismo", null=True, blank=True)
    
    LOCAL_BATISMO_CHOICES = [
        ('2ibca', 'Na 2ª IBCA'),
        ('outra', 'Em Outra Igreja'),
    ]
    local_batismo = models.CharField(
        max_length=10, 
        choices=LOCAL_BATISMO_CHOICES, 
        verbose_name="Onde foi o batismo?", 
        blank=True
    )
    outra_igreja_batismo = models.CharField(
        max_length=200, 
        verbose_name="Qual igreja?", 
        blank=True,
        help_text="Nome da igreja onde foi batizado"
    )
    recebido_por_aclamacao = models.BooleanField(
        default=False, 
        verbose_name="Foi recebido por aclamação na 2ª IBCA?"
    )

    membro_congregacao = models.BooleanField(
        default=False, 
        verbose_name="É membro de alguma congregação?"
    )
    qual_congregacao = models.CharField(
        max_length=150, 
        verbose_name="Qual Congregação?", 
        blank=True,
        help_text="Preencher apenas se for membro de congregação"
    )
    
    frequenta_escola_biblica = models.BooleanField(
        default=False, 
        verbose_name="Frequenta alguma classe da Escola Bíblica?"
    )
    qual_classe_escola_biblica = models.CharField(
        max_length=100, 
        verbose_name="Qual classe?", 
        blank=True,
        help_text="Preencher apenas se frequenta a Escola Bíblica"
    )

    deseja_exercer_funcao = models.BooleanField(
        default=False,
        verbose_name="Deseja exercer alguma função na 2ª IBCA?"
    )
    qual_funcao_deseja = models.TextField(
        verbose_name="Qual função ou ministério?",
        blank=True
    )
    
    # --- PAPÉIS E CONTROLE DO SISTEMA ---
    PAPEL_CHOICES = [
        ('congregado', 'Congregado'),
        ('membro', 'Membro'),
        ('secretario', 'Secretário'),
    ]
    papel = models.CharField(
        max_length=20, 
        choices=PAPEL_CHOICES, 
        default='congregado',
        verbose_name="Papel no Sistema"
    )
    
    data_cadastro = models.DateTimeField(default=timezone.now, verbose_name="Data de Cadastro")
    ativo = models.BooleanField(default=True, verbose_name="Usuário Ativo")
    
    aprovado = models.BooleanField(default=False, verbose_name="Cadastro Aprovado")
    aprovado_por = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Aprovado por",
        related_name='usuarios_aprovados'
    )
    data_aprovacao = models.DateTimeField(null=True, blank=True, verbose_name="Data de Aprovação")
    
    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ['nome_completo']
    
    def __str__(self):
        return self.nome_completo or self.username
    
    def save(self, *args, **kwargs):
        if not self.nome_completo:
            self.nome_completo = self.username
        # Normaliza CPF para conter apenas dígitos antes de salvar
        if self.cpf:
            self.cpf = ''.join(filter(str.isdigit, self.cpf))
        super().save(*args, **kwargs)
    
    @property
    def is_secretario(self):
        return self.papel == 'secretario'
    
    @property
    def is_membro(self):
        return self.papel == 'membro'
    
    @property
    def is_congregado(self):
        return self.papel == 'congregado'


class Filho(models.Model):
    """
    Modelo para armazenar informações dos filhos de um usuário.
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='filhos',
        verbose_name="Usuário"
    )
    nome_completo = models.CharField(max_length=200, verbose_name="Nome do Filho(a)")
    data_nascimento = models.DateField(verbose_name="Data de Nascimento")

    class Meta:
        verbose_name = "Filho"
        verbose_name_plural = "Filhos"
        ordering = ['data_nascimento']

    def __str__(self):
        return f"{self.nome_completo} (Filho de {self.user.nome_completo})"