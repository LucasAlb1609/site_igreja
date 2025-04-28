from django.shortcuts import render

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

