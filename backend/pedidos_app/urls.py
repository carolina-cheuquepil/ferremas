from django.urls import path
from .views_pedidos.estado_views import listar_estados, obtener_estado
from .views_pedidos.pedido_views import listar_pedidos, obtener_pedido, crear_pedido, actualizar_pedido, eliminar_pedido
from .views_pedidos.historial_views import (actualizar_estado_pedido_put, actualizar_estado_pedido_patch, 
crear_estado_pedido, listar_estados_pedido, obtener_estado_pedido, eliminar_estado_pedido)
from .views_pedidos.detalle_views import (crear_detalle_pedido, listar_detalles_pedido, obtener_detalle_pedido,
actualizar_detalle_pedido_patch, actualizar_detalle_pedido_put, eliminar_detalle_pedido)
from .views import (agregar_producto_al_carrito,ver_carrito, ver_carrito_html, detalle_pedido_view, 
actualizar_estado_pedido, actualizar_entrega, historial_pedidos, seleccionar_pago, pago_efectivo, pago_transferencia)

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
    path('carrito/html/<int:cliente_id>/', ver_carrito_html, name='ver_carrito_html'), #TRABAJAR 05 DE JULIO
    path('pedidos/actualizar_entrega/<int:pedido_id>/', actualizar_entrega, name='actualizar_entrega'),
    path('pedido/<int:pedido_id>/', detalle_pedido_view, name='detalle_pedido'), #Parte 6 Pendiente!!!!!!
    #Funcionalidad de actualizar estado del pedido
    path('pedido/<int:pedido_id>/estado/', actualizar_estado_pedido, name='actualizar_estado_pedido'), #parte 5
    path('historial/<int:cliente_id>/', historial_pedidos, name='historial_pedidos'), #parte 7
    path('pagos/seleccionar/<int:pedido_id>/', seleccionar_pago, name='seleccionar_pago'),
    path('pagos/efectivo/<int:pedido_id>/', pago_efectivo, name='pago_efectivo'),
    path('transferencia/<int:pedido_id>/', pago_transferencia, name='pago_transferencia'),





]
