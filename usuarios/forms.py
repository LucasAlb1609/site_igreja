# usuarios/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Filho

class FilhoForm(forms.ModelForm):
    """
    Formulário para os dados de um filho.
    """
    class Meta:
        model = Filho
        fields = ['nome_completo', 'data_nascimento']
        widgets = {
            'nome_completo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo do filho(a)'
            }),
            'data_nascimento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }

class CadastroUsuarioForm(UserCreationForm):
    """
    Formulário de cadastro de usuário baseado na ficha de cadastro da igreja.
    """
    
    # --- CAMPOS OBRIGATÓRIOS (herdados e customizados) ---
    nome_completo = forms.CharField(
        max_length=200, label="Nome Completo",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu nome completo'})
    )
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu e-mail'})
    )
    
    # --- DADOS PESSOAIS ---
    foto_perfil = forms.ImageField(label="Foto para Perfil", required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    data_nascimento = forms.DateField(label="Data de Nascimento", widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=True)
    nome_pai = forms.CharField(label="Nome do Pai", max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    nome_mae = forms.CharField(label="Nome da Mãe", max_length=200, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    cpf = forms.CharField(label="CPF", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apenas números'}), required=True)
    rg = forms.CharField(label="RG", max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    naturalidade = forms.CharField(label="Natural da cidade de:", max_length=150, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    estado_civil = forms.ChoiceField(
        choices=[('', 'Selecione...')] + User.ESTADO_CIVIL_CHOICES,
        label="Estado Civil", widget=forms.Select(attrs={'class': 'form-control'}), required=False
    )
    nome_conjuge = forms.CharField(label="Nome do Cônjuge", max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    data_casamento = forms.DateField(label="Data de Casamento", widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=False)

    # --- CORREÇÃO APLICADA AQUI ---
    tem_filhos = forms.TypedChoiceField(
        choices=[(True, 'Sim'), (False, 'Não')],
        label="Possui filhos?",
        coerce=lambda x: x == 'True', # Converte o texto 'True'/'False' para booleano
        widget=forms.RadioSelect,
        required=True
    )

    tem_alergia_medicacao = forms.TypedChoiceField(
        choices=[(True, 'Sim'), (False, 'Não')],
        label="Alergia a medicação?",
        coerce=lambda x: x == 'True',
        widget=forms.RadioSelect,
        initial=False,
        required=True
    )
    alergias_texto = forms.CharField(label="Quais alergias?", required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    
    # --- CONTATO ---
    telefone = forms.CharField(label="Telefone", max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(XX) XXXXX-XXXX'}))
    
    # --- ENDEREÇO ---
    endereco = forms.CharField(label="Endereço", max_length=300, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rua, número, complemento'}))
    bairro = forms.CharField(label="Bairro", max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    cidade = forms.CharField(label="Cidade", max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    cep = forms.CharField(label="CEP", max_length=10, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'XXXXX-XXX'}))
    
    # --- PROFISSÃO E EDUCAÇÃO ---
    profissao = forms.CharField(label="Profissão", max_length=150, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    nivel_escolar = forms.ChoiceField(
        choices=[('', 'Selecione...')] + User.NIVEL_ESCOLAR_CHOICES,
        label="Nível Escolar", widget=forms.Select(attrs={'class': 'form-control'}), required=False
    )
    
    # --- INFORMAÇÕES ECLESIÁSTICAS ---
    data_conversao = forms.DateField(label="Data de Conversão", widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=False)
    data_conversao_nao_lembro = forms.BooleanField(label="Não lembro a data", required=False)
    
    batizado_aguas = forms.BooleanField(label="É batizado nas águas?", required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    data_batismo = forms.DateField(label="Data do Batismo", widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=False)
    local_batismo = forms.ChoiceField(
        choices=[('', 'Selecione...')] + User.LOCAL_BATISMO_CHOICES,
        label="Onde foi o batismo?", widget=forms.Select(attrs={'class': 'form-control'}), required=False
    )
    outra_igreja_batismo = forms.CharField(label="Qual igreja?", max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    recebido_por_aclamacao = forms.BooleanField(label="Recebido por Aclamação na 2ª IBCA?", required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    membro_congregacao = forms.BooleanField(label="É membro de alguma congregação?", required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    qual_congregacao = forms.CharField(label="Qual congregação?", max_length=150, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    frequenta_escola_biblica = forms.BooleanField(label="Frequenta alguma classe da Escola Bíblica?", required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    qual_classe_escola_biblica = forms.CharField(label="Qual classe?", max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    deseja_exercer_funcao = forms.BooleanField(label="Deseja exercer alguma função na 2ª IBCA?", required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    qual_funcao_deseja = forms.CharField(label="Qual função ou ministério?", required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))

    class Meta:
        model = User
        fields = [
            'username', 'nome_completo', 'email', 'password1', 'password2',
            'foto_perfil', 'data_nascimento', 'nome_pai', 'nome_mae', 'cpf', 'rg', 'naturalidade',
            'estado_civil', 'nome_conjuge', 'data_casamento', 'tem_filhos', 
            'tem_alergia_medicacao', 'alergias_texto',
            'telefone', 'endereco', 'bairro', 'cidade', 'cep',
            'profissao', 'nivel_escolar',
            'data_conversao', 'data_conversao_nao_lembro',
            'batizado_aguas', 'data_batismo', 'local_batismo',
            'outra_igreja_batismo', 'recebido_por_aclamacao',
            'membro_congregacao', 'qual_congregacao',
            'frequenta_escola_biblica', 'qual_classe_escola_biblica',
            'deseja_exercer_funcao', 'qual_funcao_deseja'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customizar campos herdados
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Digite um nome de usuário'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Digite uma senha'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirme a senha'})
        self.fields['username'].label = "Nome de Usuário"
        self.fields['password1'].label = "Senha"
        self.fields['password2'].label = "Confirmar Senha"

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if cpf:
            cpf_limpo = ''.join(filter(str.isdigit, cpf))
            if len(cpf_limpo) != 11:
                raise forms.ValidationError("CPF deve conter 11 dígitos.")
            if User.objects.filter(cpf=cpf_limpo).exists():
                raise forms.ValidationError("Este CPF já está cadastrado no sistema.")
            return cpf_limpo
        return cpf

    def clean(self):
        cleaned_data = super().clean()
        
        # Validação da Data de Conversão
        data_conversao = cleaned_data.get('data_conversao')
        nao_lembro = cleaned_data.get('data_conversao_nao_lembro')
        if not data_conversao and not nao_lembro:
            self.add_error('data_conversao', 'Por favor, informe a data ou marque a opção "Não lembro".')
        if data_conversao and nao_lembro:
            self.add_error('data_conversao', 'Informe a data OU marque "Não lembro", não ambos.')

        # Validações condicionais
        if cleaned_data.get('estado_civil') == 'casado':
            if not cleaned_data.get('nome_conjuge'):
                self.add_error('nome_conjuge', "Este campo é obrigatório para pessoas casadas.")
            if not cleaned_data.get('data_casamento'):
                self.add_error('data_casamento', "Este campo é obrigatório para pessoas casadas.")
        
        # --- CORREÇÃO: O campo 'tem_alergia_medicacao' agora é um booleano (True/False) ---
        if cleaned_data.get('tem_alergia_medicacao') is True and not cleaned_data.get('alergias_texto'):
            self.add_error('alergias_texto', "Por favor, especifique as alergias.")
            
        if cleaned_data.get('batizado_aguas'):
            if not cleaned_data.get('data_batismo'):
                self.add_error('data_batismo', "Este campo é obrigatório para quem é batizado.")
            if not cleaned_data.get('local_batismo'):
                self.add_error('local_batismo', "Este campo é obrigatório para quem é batizado.")

        if cleaned_data.get('local_batismo') == 'outra' and not cleaned_data.get('outra_igreja_batismo'):
            self.add_error('outra_igreja_batismo', "Por favor, informe o nome da outra igreja.")

        if cleaned_data.get('membro_congregacao') and not cleaned_data.get('qual_congregacao'):
            self.add_error('qual_congregacao', "Por favor, informe o nome da congregação.")
            
        if cleaned_data.get('frequenta_escola_biblica') and not cleaned_data.get('qual_classe_escola_biblica'):
            self.add_error('qual_classe_escola_biblica', "Por favor, informe o nome da classe.")

        if cleaned_data.get('deseja_exercer_funcao') and not cleaned_data.get('qual_funcao_deseja'):
            self.add_error('qual_funcao_deseja', "Por favor, especifique a função ou ministério desejado.")
            
        return cleaned_data

    def save(self, commit=True):
        # A lógica customizada de conversão não é mais necessária aqui
        # pois o TypedChoiceField já entrega o valor como booleano.
        user = super().save(commit=False)
        
        # Se 'Não lembro' foi marcado, garantir que a data de conversão seja nula
        if self.cleaned_data.get('data_conversao_nao_lembro'):
            user.data_conversao = None

        # Definir padrões do sistema
        user.papel = 'congregado'
        user.aprovado = False
        user.ativo = True
        
        if commit:
            user.save()
        
        return user