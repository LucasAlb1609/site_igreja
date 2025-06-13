from django.shortcuts import render
from .models import ConfiguracaoSite, Departamento, SecaoLideranca, DiaSemana, EventoEspecial, Evento
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

# --- VIEW ATUALIZADA APENAS PARA DEPARTAMENTOS --- 
def departamentos(request):
    # Buscar todos os departamentos ordenados conforme definido no Meta do modelo
    todos_departamentos = Departamento.objects.all()
    
    # Agrupar por categoria para fácil iteração no template
    departamentos_por_categoria = {}
    categorias_existentes = [] # Para gerar as abas apenas das categorias com departamentos
    
    for dept in todos_departamentos:
        categoria_chave = dept.categoria # Ex: "TREINAMENTO"
        categoria_display = dept.get_categoria_display() # Ex: "Ministério de Treinamento..."
        
        if categoria_chave not in departamentos_por_categoria:
            departamentos_por_categoria[categoria_chave] = {"nome_display": categoria_display, "lista": []}
            # Adiciona a categoria à lista para as abas, garantindo unicidade e ordem
            if (categoria_chave, categoria_display) not in categorias_existentes:
                 categorias_existentes.append((categoria_chave, categoria_display))
                 
        departamentos_por_categoria[categoria_chave]["lista"].append(dept)
        
    # Ordenar as categorias existentes (opcional, mas pode ser útil)
    # Exemplo: Ordenar alfabeticamente pelo nome display
    categorias_existentes.sort(key=lambda item: item[1])

    context = {
        "departamentos_agrupados": departamentos_por_categoria,
        "categorias_para_abas": categorias_existentes 
    }
    return render(request, "home/departamentos.html", context)


def congregacoes(request):
    return render(request, 'congregacoes.html')

def lideranca(request):
    # Busca todas as seções, ordenadas pela ordem definida
    secoes = SecaoLideranca.objects.prefetch_related('pessoas').all()
    context = {
        'secoes': secoes
    }
    return render(request, 'lideranca.html', context)

def agenda(request):
    dias_semana = DiaSemana.objects.prefetch_related('eventos').all()
    eventos_especiais = EventoEspecial.objects.all()
    context = {
        'dias_semana': dias_semana,
        'eventos_especiais': eventos_especiais,
    }
    return render(request, 'agenda.html', context)