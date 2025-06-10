"""
URL configuration for site_igreja project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Esta linha direciona todas as URLs principais (como 'historia', etc.)
    # para serem gerenciadas pelo arquivo 'urls.py' do app 'home'.
    # Isso significa que todas as URLs que começam com 'historia', 'lideranca', etc.
    # serão tratadas pelo sistema de URLs do app 'home'.
    path('', include('home.urls')),
]
