from django.shortcuts import render
from .models import ConfiguracaoSite
from django.conf import settings

def index(request):
    # Tenta obter a configuração do site
    try:
        configuracao = ConfiguracaoSite.objects.first()
    except:
        # Se não existir ou ocorrer erro, cria um objeto vazio com valores padrão
        class DefaultConfig:
            titulo_video = 'Última Transmissão ao Vivo'
            link_youtube = 'https://www.youtube.com/watch?v=uXMkc5owHzY'  # Link padrão
            tipo_imagem = 'capa-maravilhas'
            
            def get_imagem_url(self ):
                return f"{settings.STATIC_URL}fotos/{self.tipo_imagem}.jpeg"
        
        configuracao = DefaultConfig()
    
    # Passa a configuração para o template
    context = {
        'configuracao': configuracao
    }
    
    return render(request, 'home/index.html', context)

def historia(request):
    return render(request, 'historia.html')

def lideranca(request):
    return render(request, 'lideranca.html')

def departamentos(request):
    return render(request, 'departamentos.html')

def congregacoes(request):
    return render(request, 'congregacoes.html')
