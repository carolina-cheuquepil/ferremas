# 4.- JPARepository / ORM Objects: Consulta a BD
"""
public interface CategoriaRepository extends JpaRepository<CategoriaEntity, Long> {
}
"""

#FRONEND 1
from django.shortcuts import render
from .models import Producto, Marca, HistorialInventario, Sucursal

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

    return render(request, 'inventario.html', {
        'sucursal': sucursal,
        'inventario': inventario
    })
