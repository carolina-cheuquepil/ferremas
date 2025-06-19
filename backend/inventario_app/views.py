# 4.- JPARepository / ORM Objects: Consulta a BD
"""
public interface CategoriaRepository extends JpaRepository<CategoriaEntity, Long> {
}
"""
#FRONEND 1: Categoría, Producto, Marca
#HistorialInventario
#Sucursal
from django.shortcuts import render
from .models import Producto, Marca, HistorialInventario, Sucursal
from utils.divisas import obtener_valor_dolar
from pedidos_app.models import Pedido, EstadoPedido, DetallePedido
from inventario_app.models import HistorialInventario
from datetime import datetime

def inventario_por_sucursal(request, sucursal_id):
    sucursal = Sucursal.objects.get(pk=sucursal_id)
    
    # Lista de productos con su stock total en esa sucursal
    productos = Producto.objects.all()
    inventario = []

    for prod in productos:
        movimientos = HistorialInventario.objects.filter(producto_id=prod.producto_id, sucursal_id=sucursal_id)
        stock = 0
        for m in movimientos:
            if m.tipo_movimiento == 'entrada':
                stock += m.cantidad
            elif m.tipo_movimiento == 'salida':
                stock -= m.cantidad

        inventario.append({
            'producto_id': prod.producto_id,
            'nombre': prod.nombre_producto,
            'marca': prod.marca.nombre_marca,
            'precio': prod.precio,
            'stock': stock
        })

    return render(request, 'pagina/inventario.html', {
        'sucursal': sucursal,
        'inventario': inventario
    })


def lista_productos(request):
    productos = Producto.objects.select_related('marca').all()
    valor_dolar = obtener_valor_dolar()

    lista = []
    for prod in productos:
        lista.append({
            'producto_id': prod.producto_id,
            'nombre_producto': prod.nombre_producto,
            'modelo': prod.modelo,
            'precio': prod.precio,
            'precio_usd': round(prod.precio / valor_dolar, 2) if valor_dolar > 0 else None,
            'codigo_sku': prod.codigo_sku,
            'imagen': prod.imagen,
            'marca': prod.marca.nombre_marca,
        })

    return render(request, 'pagina/productos.html', {'productos': lista})
#FRONEND PASO 1
def sistema_bodega(request):
    pedidos = Pedido.objects.all()
    inventarios = HistorialInventario.objects.all()

    # Obtener el último estado de cada pedido
    estado_actual = {}
    for pedido in pedidos:
        ultimo_estado = EstadoPedido.objects.filter(pedido=pedido).order_by('-fecha').first()
        if ultimo_estado:
            estado_actual[pedido.pedido_id] = ultimo_estado.estado.nombre_estado
        else:
            estado_actual[pedido.pedido_id] = "Sin estado"

    return render(request, 'pagina/sistema.html', {
        'pedidos': pedidos,
        'inventarios': inventarios,
        'estado_actual': estado_actual
    })

def descontar_stock_por_pedido(pedido):
    detalles = DetallePedido.objects.filter(pedido_id=pedido.pedido_id)

    for item in detalles:
        HistorialInventario.objects.create(
            producto_id=item.producto_id,
            sucursal_id=pedido.sucursal_id,  # O asigna correctamente
            cantidad=item.cantidad,
            tipo_movimiento='salida',
            fecha=datetime.now(),
            detalle=f'Salida por pedido #{pedido.pedido_id}'
        )










