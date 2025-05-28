"""
URL configuration for backend project.

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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventario_app.urls')),  # Conecta la app
    path('api/', include('usuarios_app.urls')),
    path('pedidos/', include('pedidos_app.urls')),
    path('pagos/', include('pagos_app.urls')),  # Ajusta "pago_app" al nombre real de tu app
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Agregar esta línea para servir imágenes en desarrollo - PASO 2
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)