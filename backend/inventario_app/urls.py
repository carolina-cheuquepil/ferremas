from django.urls import path
from . import views
from .views import crear_producto, producto_por_id, actualizar_producto, eliminar_producto

urlpatterns = [
    path('productos/', views.productos_api, name='productos_api'),
    path('productos/crear/', crear_producto, name='crear_producto'),
    path('productos/<int:id>/', producto_por_id, name='producto_por_id'),
    path('productos/<int:id>/actualizar/', actualizar_producto, name='actualizar_producto'),
    path('productos/<int:id>/eliminar/', eliminar_producto, name='eliminar_producto'),
]

