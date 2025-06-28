from django.urls import path
from .view_tablas.cliente_views import (ClienteListView, crear_cliente, obtener_cliente_por_id, 
actualizar_cliente, eliminar_cliente, login_cliente)
from .view_tablas.usuario_views import get_all_usuarios, get_by_id, crear_usuario, actualizar_usuario, eliminar_usuario
from .views import (login_view, registro_view, logout_view, login_trabajador_view, lista_usuarios_view, 
crear_usuario_form, editar_usuario_view, eliminar_usuario_view, sistema_vendedor)

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
    # Frontend 3
    path('clientes/login/', login_cliente, name='login_cliente'),
    path('clientes/login/form/', login_view, name='login_form'), #Parte 3: Login de cliente 😊
    path('clientes/registro/form/', registro_view, name='registro_cliente'), #Parte 2:Registro de cliente 🤗
    path('clientes/logout/', logout_view, name='logout'),
    #probando-------------------------------------------
    path('bodega/login/', login_trabajador_view, name='login_trabajador'),
    path('empleados/', lista_usuarios_view, name='lista_usuarios'),
    path('empleados/crear/', crear_usuario_form, name='crear_usuario_form'), 
    path('empleados/<int:usuario_id>/editar/', editar_usuario_view, name='editar_usuario_form'),
    path('empleados/<int:usuario_id>/eliminar/', eliminar_usuario_view, name='eliminar_usuario_form'),
    path('ventas/', sistema_vendedor, name='sistema_vendedor'),
]


