# usuarios/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
from django.db import transaction
from .forms import CadastroUsuarioForm, FilhoForm, PerfilUsuarioForm
from .models import User, Filho
import json

@transaction.atomic
def cadastro_usuario(request):
    """
    View para cadastro de novos usuários, incluindo o formset para filhos.
    """
    FilhoFormSet = formset_factory(FilhoForm, extra=1, can_delete=False)

    if request.method == 'POST':
        form = CadastroUsuarioForm(request.POST, request.FILES)
        filhos_formset = FilhoFormSet(request.POST, prefix='filhos')

        if form.is_valid() and filhos_formset.is_valid():
            try:
                user = form.save()
                for filho_form in filhos_formset:
                    if filho_form.has_changed():
                        filho = filho_form.save(commit=False)
                        filho.user = user
                        filho.save()
                messages.success(
                    request, 
                    'Cadastro realizado com sucesso! Seu cadastro está aguardando aprovação de um secretário.'
                )
                return redirect('usuarios:cadastro_sucesso')
            except Exception as e:
                messages.error(request, f'Erro ao realizar cadastro: {str(e)}')
        else:
            # LÓGICA DE DEPURAÇÃO DE ERROS RESTAURADA
            error_list = []
            if form.errors:
                for field, errors in form.errors.items():
                    # Usamos form.fields[field].label para pegar o rótulo do campo, que é mais amigável
                    field_label = form.fields[field].label if field in form.fields else field
                    error_list.append(f'Campo "{field_label}": {", ".join(errors)}')
            
            if filhos_formset.errors:
                for i, form_errors in enumerate(filhos_formset.errors):
                    if form_errors:
                        for field, errors in form_errors.items():
                            field_label = FilhoForm.base_fields[field].label if field in FilhoForm.base_fields else field
                            error_list.append(f'Filho #{i+1}, campo "{field_label}": {", ".join(errors)}')

            error_message = (
                "Por favor, corrija os erros abaixo. Detalhes: " + 
                "; ".join(error_list) if error_list 
                else "Ocorreu um erro de validação não identificado."
            )
            messages.error(request, error_message)
            # FIM DA LÓGICA DE DEPURAÇÃO RESTAURADA

    else:
        form = CadastroUsuarioForm()
        filhos_formset = FilhoFormSet(prefix='filhos')
    
    context = {
        'form': form,
        'filhos_formset': filhos_formset,
        'page_title': 'Ficha Cadastral de Novo Membro',
        'button_text': 'Cadastrar'
    }
    return render(request, 'usuarios/cadastro.html', context)

# NOVA VIEW PARA EDIÇÃO DE PERFIL
@login_required
@transaction.atomic
def editar_perfil(request):
    """
    View para o usuário editar o próprio perfil.
    """
    FilhoFormSet = inlineformset_factory(
        User, Filho, form=FilhoForm, 
        extra=1, can_delete=True,
    )

    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST, request.FILES, instance=request.user)
        formset = FilhoFormSet(request.POST, instance=request.user, prefix='filhos')
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('usuarios:perfil')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')

    else:
        form = PerfilUsuarioForm(instance=request.user)
        formset = FilhoFormSet(instance=request.user, prefix='filhos')

    context = {
        'form': form,
        'filhos_formset': formset,
        'page_title': 'Editar Meu Perfil',
        'button_text': 'Salvar Alterações'
    }
    return render(request, 'usuarios/cadastro.html', context)


def cadastro_sucesso(request):
    """
    View exibida após cadastro bem-sucedido.
    """
    return render(request, 'usuarios/cadastro_sucesso.html')


@login_required
def perfil_usuario(request):
    """
    View para exibir o perfil do usuário logado.
    """
    return render(request, 'usuarios/perfil.html', {'user': request.user})


@login_required
def dashboard(request):
    """
    Dashboard principal após login, com funcionalidades específicas por papel.
    """
    user = request.user
    
    context = {
        'user': user,
        'is_secretario': user.is_secretario,
        'is_membro': user.is_membro,
        'is_congregado': user.is_congregado,
    }
    
    # Se for secretário, adicionar estatísticas
    if user.is_secretario:
        context.update({
            'total_usuarios': User.objects.count(),
            'usuarios_pendentes': User.objects.filter(aprovado=False).count(),
            'total_membros': User.objects.filter(papel='membro').count(),
            'total_congregados': User.objects.filter(papel='congregado').count(),
        })
    
    return render(request, 'usuarios/dashboard.html', context)


@login_required
def listar_usuarios_pendentes(request):
    """
    View para secretários visualizarem usuários pendentes de aprovação.
    """
    # Verificar se o usuário é secretário
    if not request.user.is_secretario:
        messages.error(request, 'Acesso negado. Apenas secretários podem acessar esta página.')
        return redirect('usuarios:dashboard')
    
    usuarios_pendentes = User.objects.filter(aprovado=False).order_by('-data_cadastro')
    
    return render(request, 'usuarios/usuarios_pendentes.html', {
        'usuarios_pendentes': usuarios_pendentes
    })


@login_required
def aprovar_usuario(request, user_id):
    """
    View para secretários aprovarem usuários.
    """
    if not request.user.is_secretario:
        messages.error(request, 'Acesso negado.')
        return redirect('usuarios:dashboard')
    
    try:
        usuario = User.objects.get(id=user_id)
        
        # Se há um papel especificado no POST, usar esse papel
        if request.method == 'POST':
            novo_papel = request.POST.get('papel')
            if novo_papel in ['congregado', 'membro', 'secretario']:
                usuario.papel = novo_papel
        
        usuario.aprovado = True
        usuario.aprovado_por = request.user
        from django.utils import timezone
        usuario.data_aprovacao = timezone.now()
        usuario.save()
        
        messages.success(request, f'Usuário {usuario.nome_completo} aprovado com sucesso como {usuario.get_papel_display()}!')
    except User.DoesNotExist:
        messages.error(request, 'Usuário não encontrado.')
    
    return redirect('usuarios:usuarios_pendentes')


@login_required
def rejeitar_usuario(request, user_id):
    """
    View para secretários rejeitarem usuários.
    """
    if not request.user.is_secretario:
        messages.error(request, 'Acesso negado.')
        return redirect('usuarios:dashboard')
    
    try:
        usuario = User.objects.get(id=user_id)
        usuario.delete()
        
        messages.success(request, f'Cadastro de {usuario.nome_completo} foi rejeitado e removido.')
    except User.DoesNotExist:
        messages.error(request, 'Usuário não encontrado.')
    
    return redirect('usuarios:usuarios_pendentes')


@login_required
def alterar_papel_usuario(request, user_id):
    """
    View para secretários alterarem o papel de usuários aprovados.
    """
    if not request.user.is_secretario:
        messages.error(request, 'Acesso negado.')
        return redirect('usuarios:dashboard')
    
    if request.method == 'POST':
        novo_papel = request.POST.get('papel')
        
        if novo_papel in ['congregado', 'membro', 'secretario']:
            try:
                usuario = User.objects.get(id=user_id)
                usuario.papel = novo_papel
                usuario.save()
                
                messages.success(request, f'Papel de {usuario.nome_completo} alterado para {usuario.get_papel_display()}.')
            except User.DoesNotExist:
                messages.error(request, 'Usuário não encontrado.')
        else:
            messages.error(request, 'Papel inválido.')
    
    return redirect('usuarios:usuarios_pendentes')

@login_required
def listar_todos_usuarios(request):
    """
    View para secretários visualizarem todos os usuários (aprovados e pendentes).
    """
    if not request.user.is_secretario:
        messages.error(request, 'Acesso negado. Apenas secretários podem acessar esta página.')
        return redirect('usuarios:dashboard')
    
    usuarios = User.objects.all().order_by('nome_completo')
    
    context = {
        'usuarios': usuarios,
        'page_title': 'Lista de Usuários'
    }
    return render(request, 'usuarios/listar_usuarios.html', context)




@login_required
@transaction.atomic
def criar_usuario(request):
    """
    View para secretários criarem novos usuários diretamente.
    """
    if not request.user.is_secretario:
        messages.error(request, 'Acesso negado. Apenas secretários podem acessar esta página.')
        return redirect('usuarios:dashboard')
    
    FilhoFormSet = formset_factory(FilhoForm, extra=1, can_delete=False)

    if request.method == 'POST':
        form = CadastroUsuarioForm(request.POST, request.FILES)
        filhos_formset = FilhoFormSet(request.POST, prefix='filhos')

        if form.is_valid() and filhos_formset.is_valid():
            try:
                user = form.save(commit=False)
                user.aprovado = True  # Usuários criados por secretários são automaticamente aprovados
                user.aprovado_por = request.user
                user.data_aprovacao = timezone.now()
                user.save()
                
                for filho_form in filhos_formset:
                    if filho_form.has_changed():
                        filho = filho_form.save(commit=False)
                        filho.user = user
                        filho.save()
                        
                messages.success(request, f'Usuário {user.nome_completo} criado com sucesso!')
                return redirect('usuarios:listar_todos_usuarios')
            except Exception as e:
                messages.error(request, f'Erro ao criar usuário: {str(e)}')
        else:
            # Lógica de depuração de erros
            error_list = []
            if form.errors:
                for field, errors in form.errors.items():
                    field_label = form.fields[field].label if field in form.fields else field
                    error_list.append(f'Campo "{field_label}": {", ".join(errors)}')
            
            if filhos_formset.errors:
                for i, form_errors in enumerate(filhos_formset.errors):
                    if form_errors:
                        for field, errors in form_errors.items():
                            field_label = FilhoForm.base_fields[field].label if field in FilhoForm.base_fields else field
                            error_list.append(f'Filho #{i+1}, campo "{field_label}": {", ".join(errors)}')

            error_message = (
                "Por favor, corrija os erros abaixo. Detalhes: " + 
                "; ".join(error_list) if error_list 
                else "Ocorreu um erro de validação não identificado."
            )
            messages.error(request, error_message)

    else:
        form = CadastroUsuarioForm()
        filhos_formset = FilhoFormSet(prefix='filhos')
    
    context = {
        'form': form,
        'filhos_formset': filhos_formset,
        'page_title': 'Criar Novo Usuário',
        'button_text': 'Criar Usuário'
    }
    return render(request, 'usuarios/cadastro.html', context)


@login_required
@transaction.atomic
def editar_usuario(request, user_id):
    """
    View para secretários editarem usuários existentes.
    """
    if not request.user.is_secretario:
        messages.error(request, 'Acesso negado. Apenas secretários podem acessar esta página.')
        return redirect('usuarios:dashboard')
    
    try:
        usuario = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'Usuário não encontrado.')
        return redirect('usuarios:listar_todos_usuarios')
    
    FilhoFormSet = inlineformset_factory(
        User, Filho, form=FilhoForm, 
        extra=1, can_delete=True,
    )

    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST, request.FILES, instance=usuario)
        formset = FilhoFormSet(request.POST, instance=usuario, prefix='filhos')
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, f'Usuário {usuario.nome_completo} atualizado com sucesso!')
            return redirect('usuarios:listar_todos_usuarios')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')

    else:
        form = PerfilUsuarioForm(instance=usuario)
        formset = FilhoFormSet(instance=usuario, prefix='filhos')

    context = {
        'form': form,
        'filhos_formset': formset,
        'page_title': f'Editar Usuário: {usuario.nome_completo}',
        'button_text': 'Salvar Alterações',
        'usuario': usuario
    }
    return render(request, 'usuarios/cadastro.html', context)


@login_required
def excluir_usuario(request, user_id):
    """
    View para secretários excluírem usuários.
    """
    if not request.user.is_secretario:
        messages.error(request, 'Acesso negado. Apenas secretários podem acessar esta página.')
        return redirect('usuarios:dashboard')
    
    try:
        usuario = User.objects.get(id=user_id)
        
        # Não permitir que o secretário exclua a si mesmo
        if usuario == request.user:
            messages.error(request, 'Você não pode excluir sua própria conta.')
            return redirect('usuarios:listar_todos_usuarios')
        
        # Não permitir exclusão de superusuários
        if usuario.is_superuser:
            messages.error(request, 'Não é possível excluir superusuários.')
            return redirect('usuarios:listar_todos_usuarios')
        
        nome_usuario = usuario.nome_completo
        usuario.delete()
        messages.success(request, f'Usuário {nome_usuario} foi excluído com sucesso.')
        
    except User.DoesNotExist:
        messages.error(request, 'Usuário não encontrado.')
    
    return redirect('usuarios:listar_todos_usuarios')


@login_required
def ver_usuario(request, user_id):
    """
    View para secretários visualizarem detalhes de um usuário específico.
    """
    if not request.user.is_secretario:
        messages.error(request, 'Acesso negado. Apenas secretários podem acessar esta página.')
        return redirect('usuarios:dashboard')
    
    try:
        usuario = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'Usuário não encontrado.')
        return redirect('usuarios:listar_todos_usuarios')
    
    context = {
        'user': usuario,
        'page_title': f'Perfil de {usuario.nome_completo}',
        'is_viewing_other': True
    }
    return render(request, 'usuarios/perfil.html', context)

