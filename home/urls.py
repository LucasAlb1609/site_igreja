from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path("historia/", views.historia, name="historia"),
    path("lideranca/", views.lideranca, name="lideranca"),
    path("departamentos/", views.departamentos, name="departamentos"),
    path("congregacoes/", views.congregacoes, name="congregacoes"),
    path("agenda/", views.agenda, name="agenda"),
]

# Adicione isso ao final do arquivo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)