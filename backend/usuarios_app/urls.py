from django.urls import path
from .view_tablas.cliente_views import (ClienteListView, crear_cliente, obtener_cliente_por_id, 
actualizar_cliente, eliminar_cliente, login_cliente)
from .view_tablas.usuario_views import get_all_usuarios, get_by_id, crear_usuario, actualizar_usuario, eliminar_usuario
from .views import login_view, registro_view, logout_view

# path('api/', include('usuarios_app.urls'))

urlpatterns = [
    #Clientes
    path('clientes/', ClienteListView.as_view(), name='listar_clientes'),
    path('clientes/crear/', crear_cliente, name='crear_cliente'), 
    path('clientes/<int:cliente_id>/', obtener_cliente_por_id, name='obtener_cliente'),
    path('clientes/<int:cliente_id>/actualizar/', actualizar_cliente, name='actualizar_cliente'),
    path('clientes/<int:cliente_id>/eliminar/', eliminar_cliente, name='eliminar_cliente'),
    #Usuarios
    path('usuarios/', get_all_usuarios, name='listar_usuario'),
    path('usuarios/crear/', crear_usuario, name='crear_usuarios'), 
    path('usuarios/<int:usuario_id>/', get_by_id, name='obtener_usuario'),
    path('usuarios/<int:usuario_id>/actualizar/', actualizar_usuario, name='actualizar_usuario'),
    path('usuarios/<int:usuario_id>/eliminar/', eliminar_usuario, name='eliminar_usuario'),
    # Frontend
    path('clientes/login/', login_cliente, name='login_cliente'),
    path('clientes/login/form/', login_view, name='login_form'),
    path('clientes/registro/form/', registro_view, name='registro_cliente'), #Paso 2
    path('clientes/logout/', logout_view, name='logout'),

]


