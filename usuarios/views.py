# usuarios/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.db import transaction
from .forms import CadastroUsuarioForm, FilhoForm
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
                # Salva o usuário principal primeiro
                user = form.save()

                # Processa e salva os filhos
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
                messages.error(
                    request, 
                    f'Erro ao realizar cadastro: {str(e)}'
                )
        else:
            # --- LÓGICA DE DEPURAÇÃO DE ERRO ADICIONADA AQUI ---
            error_list = []
            if form.errors:
                # Adiciona erros do formulário principal
                for field, errors in form.errors.items():
                    error_list.append(f'Campo "{field}": {", ".join(errors)}')
            
            if filhos_formset.errors:
                # Adiciona erros dos formulários de filhos
                for i, form_errors in enumerate(filhos_formset.errors):
                    if form_errors:
                        for field, errors in form_errors.items():
                            error_list.append(f'Filho #{i+1}, campo "{field}": {", ".join(errors)}')

            error_message = (
                "Por favor, corrija os erros abaixo. Detalhes: " + 
                "; ".join(error_list) if error_list 
                else "Ocorreu um erro de validação não identificado."
            )
            messages.error(request, error_message)
            # --- FIM DA LÓGICA DE DEPURAÇÃO ---

    else:
        form = CadastroUsuarioForm()
        filhos_formset = FilhoFormSet(prefix='filhos')
    
    context = {
        'form': form,
        'filhos_formset': filhos_formset
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