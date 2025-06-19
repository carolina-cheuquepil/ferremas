from django.urls import path
from .views_pedidos.estado_views import listar_estados, obtener_estado
from .views_pedidos.pedido_views import listar_pedidos, obtener_pedido, crear_pedido, actualizar_pedido, eliminar_pedido
from .views_pedidos.historial_views import (actualizar_estado_pedido_put, actualizar_estado_pedido_patch, 
crear_estado_pedido, listar_estados_pedido, obtener_estado_pedido, eliminar_estado_pedido)
from .views_pedidos.detalle_views import (crear_detalle_pedido, listar_detalles_pedido, obtener_detalle_pedido,
actualizar_detalle_pedido_patch, actualizar_detalle_pedido_put, eliminar_detalle_pedido)
from .views import agregar_producto_al_carrito,ver_carrito, ver_carrito_html, detalle_pedido_view, actualizar_estado_pedido

#path('pedidos/', include('pedidos_app.urls')),
urlpatterns = [
    #estados
    path('estados/', listar_estados, name='listar_estados'),
    path('estados/<int:pk>/', obtener_estado, name='obtener_estado'),
    #pedidos
    path('pedidos/', listar_pedidos), 
    path('pedidos/<int:pk>/', obtener_pedido), 
    path('pedidos/crear/', crear_pedido), 
    path('pedidos/actualizar/<int:pk>/', actualizar_pedido),
    path('pedidos/eliminar/<int:pk>/', eliminar_pedido),
    #Estado pedido
    path('estado-pedido/actualizar/<int:pk>/', actualizar_estado_pedido_put), #Update
    path('estado-pedido/parcial/<int:pk>/', actualizar_estado_pedido_patch), #Update
    path('estado-pedido/crear/', crear_estado_pedido), #Crear
    path('estado-pedido/', listar_estados_pedido), #Read
    path('estado-pedido/<int:pk>/', obtener_estado_pedido), #Read by id
    path('estado-pedido/eliminar/<int:pk>/', eliminar_estado_pedido),
    #Detalle 
    path('detalle-pedido/crear/', crear_detalle_pedido),
    path('detalle-pedido/', listar_detalles_pedido),
    path('detalle-pedido/<int:pk>/', obtener_detalle_pedido),
    path('detalle-pedido/actualizar/<int:pk>/', actualizar_detalle_pedido_put),
    path('detalle-pedido/parcial/<int:pk>/', actualizar_detalle_pedido_patch),
    path('detalle-pedido/eliminar/<int:pk>/', eliminar_detalle_pedido),
    #Frontend 2
    path('carrito/agregar/', agregar_producto_al_carrito, name='api_agregar_carrito'),
    path('carrito/<int:cliente_id>/', ver_carrito),
    path('carrito/html/<int:cliente_id>/', ver_carrito_html),
    path('pedido/<int:pedido_id>/', detalle_pedido_view, name='detalle_pedido'),
    path('pedido/<int:pedido_id>/estado/', actualizar_estado_pedido, name='actualizar_estado_pedido'),




]
