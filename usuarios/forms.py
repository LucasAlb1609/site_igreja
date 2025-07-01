from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class CadastroUsuarioForm(UserCreationForm):
    """
    Formulário de cadastro de usuário baseado na ficha de cadastro da igreja.
    """
    
    # Campos obrigatórios
    nome_completo = forms.CharField(
        max_length=200,
        label="Nome Completo",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu nome completo'
        })
    )
    
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu e-mail'
        })
    )
    
    # Dados pessoais
    data_nascimento = forms.DateField(
        label="Data de Nascimento",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        required=False
    )
    
    estado_civil = forms.ChoiceField(
        choices=[('', 'Selecione...')] + User.ESTADO_CIVIL_CHOICES,
        label="Estado Civil",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    
    # Contato
    telefone = forms.CharField(
        max_length=15,
        label="Telefone",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '(XX) XXXXX-XXXX'
        }),
        required=False
    )
    
    # Endereço
    endereco = forms.CharField(
        max_length=300,
        label="Endereço",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rua, número, complemento'
        }),
        required=False
    )
    
    bairro = forms.CharField(
        max_length=100,
        label="Bairro",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite o bairro'
        }),
        required=False
    )
    
    cidade = forms.CharField(
        max_length=100,
        label="Cidade",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite a cidade'
        }),
        required=False
    )
    
    cep = forms.CharField(
        max_length=10,
        label="CEP",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'XXXXX-XXX'
        }),
        required=False
    )
    
    # Profissão e educação
    profissao = forms.CharField(
        max_length=150,
        label="Profissão",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua profissão'
        }),
        required=False
    )
    
    nivel_escolar = forms.ChoiceField(
        choices=[('', 'Selecione...')] + User.NIVEL_ESCOLAR_CHOICES,
        label="Nível Escolar",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    
    # Informações da igreja
    data_conversao = forms.DateField(
        label="Data de Conversão",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        required=False
    )
    
    # Membro de congregação
    membro_congregacao = forms.BooleanField(
        label="Membro de Congregação?",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        required=False
    )
    
    qual_congregacao = forms.CharField(
        max_length=150,
        label="Qual Congregação?",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome da congregação'
        }),
        required=False
    )
    
    # Como foi aceito na igreja
    aceito_por = forms.ChoiceField(
        choices=[('', 'Selecione...')] + User.ACEITO_POR_CHOICES,
        label="Aceito por",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    
    # Escola Bíblica
    frequenta_escola_biblica = forms.BooleanField(
        label="Frequenta alguma classe da Escola Bíblica?",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        required=False
    )
    
    qual_classe_escola_biblica = forms.CharField(
        max_length=100,
        label="Qual classe?",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome da classe'
        }),
        required=False
    )
    
    class Meta:
        model = User
        fields = [
            'username', 'nome_completo', 'email', 'password1', 'password2',
            'data_nascimento', 'estado_civil', 'telefone',
            'endereco', 'bairro', 'cidade', 'cep',
            'profissao', 'nivel_escolar',
            'data_conversao', 'membro_congregacao', 'qual_congregacao',
            'aceito_por', 'frequenta_escola_biblica', 'qual_classe_escola_biblica'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Customizar campos herdados do UserCreationForm
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Digite um nome de usuário'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Digite uma senha'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirme a senha'
        })
        
        # Personalizar labels
        self.fields['username'].label = "Nome de Usuário"
        self.fields['password1'].label = "Senha"
        self.fields['password2'].label = "Confirmar Senha"
    
    def clean_telefone(self):
        """Validação customizada para o campo telefone"""
        telefone = self.cleaned_data.get('telefone')
        if telefone:
            # Remove espaços e caracteres especiais para validação
            telefone_limpo = ''.join(filter(str.isdigit, telefone))
            if len(telefone_limpo) not in [10, 11]:
                raise forms.ValidationError("Telefone deve ter 10 ou 11 dígitos.")
        return telefone
    
    def clean(self):
        """Validações customizadas do formulário"""
        cleaned_data = super().clean()
        
        # Se marcou que é membro de congregação, deve informar qual
        membro_congregacao = cleaned_data.get('membro_congregacao')
        qual_congregacao = cleaned_data.get('qual_congregacao')
        
        if membro_congregacao and not qual_congregacao:
            raise forms.ValidationError(
                "Se você é membro de congregação, deve informar qual congregação."
            )
        
        # Se marcou que frequenta escola bíblica, deve informar qual classe
        frequenta_escola_biblica = cleaned_data.get('frequenta_escola_biblica')
        qual_classe_escola_biblica = cleaned_data.get('qual_classe_escola_biblica')
        
        if frequenta_escola_biblica and not qual_classe_escola_biblica:
            raise forms.ValidationError(
                "Se você frequenta a Escola Bíblica, deve informar qual classe."
            )
        
        return cleaned_data
    
    def save(self, commit=True):
        """Salvar o usuário com configurações padrão"""
        user = super().save(commit=False)
        
        # Definir papel padrão como congregado
        user.papel = 'congregado'
        
        # Usuário não aprovado por padrão (precisa de aprovação de secretário)
        user.aprovado = False
        
        # Usuário ativo por padrão
        user.ativo = True
        
        if commit:
            user.save()
        
        return user

