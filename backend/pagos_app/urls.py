from django.urls import path
from .views_tablas.pago_views import listar_pagos, crear_pago, obtener_pago_por_id, actualizar_pago, eliminar_pago
from .views import iniciar_pago, retorno_pago

#path('pagos/', include('pagos_app.urls')),
urlpatterns = [
    path('pago/', listar_pagos, name='listar_pagos'),
    path('pago/crear/', crear_pago, name='crear_pago'),
    path('pago/<int:id>/', obtener_pago_por_id, name='obtener_pago'),
    path('pago/<int:id>/actualizar/', actualizar_pago, name='actualizar_pago'),
    path('pago/<int:id>/eliminar/', eliminar_pago, name='eliminar_pago'),
    #Transacciones WebPay Transbank
    path('iniciar/<int:pedido_id>/', iniciar_pago, name='iniciar_pago'),
    path('retorno/', retorno_pago, name='retorno_pago'), #Parte 6?

]






