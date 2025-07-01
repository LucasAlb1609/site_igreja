from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    """
    Modelo de usuário personalizado baseado na ficha de cadastro da igreja.
    """
    
    # Campos básicos (alguns já existem no AbstractUser)
    nome_completo = models.CharField(max_length=200, verbose_name="Nome Completo")
    
    # Dados pessoais
    data_nascimento = models.DateField(verbose_name="Data de Nascimento", null=True, blank=True)
    
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
    
    # Contato
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
    
    # Endereço
    endereco = models.CharField(max_length=300, verbose_name="Endereço", blank=True)
    bairro = models.CharField(max_length=100, verbose_name="Bairro", blank=True)
    cidade = models.CharField(max_length=100, verbose_name="Cidade", blank=True)
    cep = models.CharField(max_length=10, verbose_name="CEP", blank=True)
    
    # Profissão e educação
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
    
    # Informações da igreja
    data_conversao = models.DateField(verbose_name="Data de Conversão", null=True, blank=True)
    
    # Membro de congregação
    membro_congregacao = models.BooleanField(
        default=False, 
        verbose_name="Membro de Congregação?"
    )
    qual_congregacao = models.CharField(
        max_length=150, 
        verbose_name="Qual Congregação?", 
        blank=True,
        help_text="Preencher apenas se for membro de congregação"
    )
    
    # Como foi aceito na igreja
    ACEITO_POR_CHOICES = [
        ('batismo', 'Batismo'),
        ('aclamacao', 'Aclamação'),
    ]
    aceito_por = models.CharField(
        max_length=20, 
        choices=ACEITO_POR_CHOICES, 
        verbose_name="Aceito por",
        blank=True
    )
    
    # Escola Bíblica
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
    
    # Papéis no sistema
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
    
    # Campos de controle
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")
    ativo = models.BooleanField(default=True, verbose_name="Usuário Ativo")
    
    # Campos para aprovação (secretários podem aprovar/rejeitar cadastros)
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
        # Se não tem nome completo, usa o username
        if not self.nome_completo:
            self.nome_completo = self.username
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

