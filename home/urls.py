from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("historia/", views.historia, name="historia"),
    path("lideranca/", views.lideranca, name="lideranca"),
    path("departamentos/", views.departamentos, name="departamentos"),
    path("congregacoes/", views.congregacoes, name="congregacoes"),
    path("agenda/", views.agenda, name="agenda"),
    path("devocionais/", views.lista_devocionais, name="lista_devocionais"),
]