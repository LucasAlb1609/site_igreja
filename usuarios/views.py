from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import CadastroUsuarioForm
from .models import User


def cadastro_usuario(request):
    """
    View para cadastro de novos usuários.
    """
    if request.method == 'POST':
        form = CadastroUsuarioForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
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
            messages.error(
                request, 
                'Por favor, corrija os erros abaixo.'
            )
    else:
        form = CadastroUsuarioForm()
    
    return render(request, 'usuarios/cadastro.html', {'form': form})


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

