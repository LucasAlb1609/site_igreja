from django.shortcuts import render
from django.views.generic import TemplateView

def index(request):
    return render(request, 'home/index.html')

def historia(request):
    return render(request, 'historia.html')

def lideranca(request):
    return render(request, 'lideranca.html')

def departamentos(request):
    return render(request, 'departamentos.html')

def congregacoes(request):
    return render(request, 'congregacoes.html')


# Alternativa com Class-Based Views
class IndexView(TemplateView):
    template_name = 'index.html'

class HistoriaView(TemplateView):
    template_name = 'historia.html'

class LiderancaView(TemplateView):
    template_name = 'lideranca.html'

class DepartamentosView(TemplateView):
    template_name = 'departamentos.html'

class CongregacoesView(TemplateView):
    template_name = 'congregacoes.html'