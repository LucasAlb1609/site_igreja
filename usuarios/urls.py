from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'usuarios'

urlpatterns = [
    # Cadastro
    path('cadastro/', views.cadastro_usuario, name='cadastro'),
    path('cadastro/sucesso/', views.cadastro_sucesso, name='cadastro_sucesso'),
    
    # Login e Logout (usando views padrão do Django)
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Dashboard e perfil
    path('dashboard/', views.dashboard, name='dashboard'),
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    
    # Gestão de usuários (para secretários)
    path('pendentes/', views.listar_usuarios_pendentes, name='usuarios_pendentes'),
    path('aprovar/<int:user_id>/', views.aprovar_usuario, name='aprovar_usuario'),
    path('rejeitar/<int:user_id>/', views.rejeitar_usuario, name='rejeitar_usuario'),
    path('alterar-papel/<int:user_id>/', views.alterar_papel_usuario, name='alterar_papel_usuario'),
    
    # Gestão completa de usuários (para secretários)
    path("todos/", views.listar_todos_usuarios, name="listar_todos_usuarios"),
    path("criar/", views.criar_usuario, name="criar_usuario"),
    path("editar/<int:user_id>/", views.editar_usuario, name="editar_usuario"),
    path("excluir/<int:user_id>/", views.excluir_usuario, name="excluir_usuario"),
    path("ver/<int:user_id>/", views.ver_usuario, name="ver_usuario"),
]

