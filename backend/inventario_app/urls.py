from django.urls import path
from .view_tablas.producto_views import productos_api, crear_producto, obtener_producto, actualizar_producto, eliminar_producto
from .view_tablas.categoria_views import listar_categorias, obtener_categoria
from .view_tablas.marca_views import all_marcas, get_by_id, crear_marca
from .view_tablas.sucursal_views import listar_sucursales, obtener_sucursal
from .view_tablas.inventario_views import get_all_inventario, crear_registro, actualizar_registro, actualizar_registro_parcial, eliminar_registro
from .views import inventario_por_sucursal, lista_productos, sistema_bodega
# path('', include('inventario_app.urls')),
urlpatterns = [
    path('productos/', productos_api, name='productos_api'),
    path('productos/crear/', crear_producto, name='crear_producto'),
    path('productos/<int:pk>/', obtener_producto, name='obtener_producto'),
    path('productos/<int:pk>/actualizar/', actualizar_producto, name='actualizar_producto'),
    path('productos/<int:pk>/eliminar/', eliminar_producto, name='eliminar_producto'),
    #Categorias
    path('categorias/', listar_categorias, name='listar_categorias'),
    path('categorias/<int:pk>/', obtener_categoria, name='obtener_categoria'),
    #Marca
    path('marcas/', all_marcas, name='marcas'),
    path('marca/<int:pk>/', get_by_id, name='marca_id'),
    path('marcas/crear/', crear_marca, name='crear_marca'),
    #Sucursales
    path('sucursales/', listar_sucursales, name='listar_sucursales'),
    path('sucursales/<int:pk>/', obtener_sucursal, name='obtener_sucursal'),
    #Historial inventario
    path('inventarios/', get_all_inventario, name='inventarios'),
    path('inventarios/crear/', crear_registro, name='crear_registro'),
    path('inventarios/actualizar/<int:movimiento_id>/', actualizar_registro, name='actualizar_inventario'),
    path('inventarios/editar/<int:movimiento_id>/', actualizar_registro_parcial),
    path('inventarios/eliminar/<int:movimiento_id>/', eliminar_registro),
    #FRONEND PASO 2
    path('inventario/<int:sucursal_id>/', inventario_por_sucursal, name='inventario_sucursal'),
    path('productos/lista/', lista_productos, name='lista_productos'), #Parte 1
    path('pedidos/', sistema_bodega, name='sistema_bodega'),
]





    

