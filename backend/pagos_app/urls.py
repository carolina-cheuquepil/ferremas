from django.urls import path
from . import views

urlpatterns = [
    path('pago/', views.listar_pagos, name='listar_pagos'),
    path('pago/crear/', views.crear_pago, name='crear_pago'),
    path('pago/<int:id>/', views.obtener_pago_por_id, name='obtener_pago'),
    path('pago/<int:id>/actualizar/', views.actualizar_pago, name='actualizar_pago'),
    path('pago/<int:id>/eliminar/', views.eliminar_pago, name='eliminar_pago'),
]
