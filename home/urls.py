from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views  # ou from sua_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Usando function-based views
    path('', views.index, name='index'),
    path('historia/', views.historia, name='historia'),
    path('lideranca/', views.lideranca, name='lideranca'),
    path('departamentos/', views.departamentos, name='departamentos'),
    path('congregacoes/', views.congregacoes, name='congregacoes'),
    
    # Ou usando class-based views
    # path('', views.IndexView.as_view(), name='index'),
    # path('historia/', views.HistoriaView.as_view(), name='historia'),
    # path('lideranca/', views.LiderancaView.as_view(), name='lideranca'),
    # path('departamentos/', views.DepartamentosView.as_view(), name='departamentos'),
    # path('congregacoes/', views.CongregacoesView.as_view(), name='congregacoes'),
]

# Configuração para servir arquivos estáticos durante o desenvolvimento
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)