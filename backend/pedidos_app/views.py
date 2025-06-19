from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from pedidos_app.models import Pedido, DetallePedido, EstadoPedido, Estado
from inventario_app.models import Producto, HistorialInventario
from inventario_app.utils.divisas import obtener_valor_dolar
from datetime import datetime
from pedidos_app.serializers import DetallePedidoSerializer
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

@api_view(['POST'])
def agregar_producto_al_carrito(request):
    cliente_id = request.user.cliente.cliente_id

    producto_id = request.data.get('producto_id')
    cantidad = int(request.data.get('cantidad', 1))

    if not cliente_id or not producto_id:
        return Response({'error': 'Faltan datos'}, status=status.HTTP_400_BAD_REQUEST)

    # Buscar un pedido pendiente del cliente
    pedido = Pedido.objects.filter(cliente_id=cliente_id, estadopedido__estado_id=1).last()

    if not pedido:
        pedido = Pedido.objects.create(
            cliente_id=cliente_id,
            sucursal_id=6,  # fijo por ahora
            fecha=datetime.now(),
            tipo_entrega='retiro',
            total=0,
            valor_dolar_usado=0,
            total_usd=0,
        )
        EstadoPedido.objects.create(
            pedido=pedido,
            estado_id=1,  # Pendiente
            fecha=datetime.now(),
            actor_id=cliente_id,
            actor_tipo='cliente',
        )

    producto = Producto.objects.get(pk=producto_id)

    # Agregar o actualizar producto en el detalle
    detalle, creado = DetallePedido.objects.get_or_create(
        pedido=pedido,
        producto_id=producto_id,
        defaults={
            'cantidad': cantidad,
            'precio_unitario': producto.precio
        }
    )

    if not creado:
        detalle.cantidad += cantidad
        detalle.save()

    # Actualizar total del pedido
    # Recalcular total del pedido
    detalles = DetallePedido.objects.filter(pedido=pedido)
    total = sum(d.cantidad * d.precio_unitario for d in detalles)

    # Valor del dólar fijo por ahora
    valor_dolar = obtener_valor_dolar()
    total_usd = round(total / valor_dolar, 2)

    # Actualizar el pedido
    pedido.total = total
    pedido.valor_dolar_usado = valor_dolar
    pedido.total_usd = total_usd
    pedido.save()

    return Response({'mensaje': 'Producto agregado al carrito correctamente'})

@api_view(['GET'])
def ver_carrito(request, cliente_id):
    try:
        pedido = Pedido.objects.filter(cliente_id=cliente_id, estadopedido__estado_id=1).last()
        if not pedido:
            return Response({'mensaje': 'No hay un carrito activo'}, status=200)

        detalles = DetallePedido.objects.filter(pedido=pedido)
        serializer = DetallePedidoSerializer(detalles, many=True)

        return Response({
            'pedido_id': pedido.pedido_id,
            'fecha': pedido.fecha,
            'tipo_entrega': pedido.tipo_entrega,
            'detalles': serializer.data
        })

    except Exception as e:
        return Response({'error': str(e)}, status=500)

def ver_carrito_html(request, cliente_id):
    pedido = Pedido.objects.filter(cliente_id=cliente_id, estadopedido__estado_id=1).last()
    if not pedido:
        return render(request, 'carrito.html', {'mensaje': 'No hay productos en el carrito'})

    detalles = DetallePedido.objects.filter(pedido=pedido)

    for d in detalles:
        d.total_linea = d.cantidad * d.precio_unitario

    return render(request, 'carrito.html', {
        'pedido': pedido,
        'detalles': detalles
    })

#Sistema interno: Ver detalle de un pedido específico

@csrf_exempt
def actualizar_estado_pedido(request, pedido_id):
    if request.method == 'POST':
        estado_id = request.POST.get('estado_id')

        EstadoPedido.objects.create(
            pedido_id=pedido_id,
            estado_id=estado_id,
            fecha=timezone.now(),
            actor_id=request.user.id,
            actor_tipo='usuario'
        )

        # 👇 Descontar stock si el estado es "Listo"
        if estado_id == '3':  # Cambia el número si tu estado "Listo" tiene otro ID
            pedido = Pedido.objects.get(pk=pedido_id)
            detalles = DetallePedido.objects.filter(pedido_id=pedido_id)

            for item in detalles:
                HistorialInventario.objects.create(
                    producto_id=item.producto_id,
                    sucursal_id=pedido.sucursal_id,  # Asegúrate de tener este campo
                    cantidad=item.cantidad,
                    tipo_movimiento='salida',
                    fecha=datetime.now(),
                    detalle=f'Salida por pedido #{pedido_id}'
                )

        messages.success(request, "✅ Estado actualizado correctamente")
        return redirect('detalle_pedido', pedido_id=pedido_id)

    

def detalle_pedido_view(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    detalles = DetallePedido.objects.filter(pedido_id=pedido_id)
    historial = EstadoPedido.objects.filter(pedido_id=pedido_id).order_by('-fecha')
    estados = Estado.objects.all()  # Para el select

    return render(request, 'pagina/detalle_pedido.html', {
        'pedido': pedido,
        'detalles': detalles,
        'historial': historial,
        'estados': estados
    })

