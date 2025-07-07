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
from pagos_app.models import Pago
import logging
from django.utils.timezone import now


@api_view(['POST'])
def agregar_producto_al_carrito(request):
    cliente_id = request.user.cliente.cliente_id
    producto_id = request.data.get('producto_id')
    cantidad = int(request.data.get('cantidad', 1))

    if not cliente_id or not producto_id:
        return Response({'error': 'Faltan datos'}, status=status.HTTP_400_BAD_REQUEST)

    # Buscar el último pedido del cliente
    pedido = Pedido.objects.filter(cliente_id=cliente_id).order_by('-fecha').first()

    # Verificar si no hay pedido o si ya no está en estado Pendiente
    if not pedido or EstadoPedido.objects.filter(pedido=pedido).order_by('-fecha').first().estado_id != 1:
        # Crear nuevo pedido
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

    # Obtener producto
    producto = Producto.objects.get(pk=producto_id)

    # Agregar o actualizar producto
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

    # Recalcular total del pedido
    detalles = DetallePedido.objects.filter(pedido=pedido)
    total = sum(d.cantidad * d.precio_unitario for d in detalles)
    valor_dolar = obtener_valor_dolar()
    total_usd = round(total / valor_dolar, 2)

    # Guardar pedido actualizado
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

#Trabajar 05/07/2025
def ver_carrito_html(request, cliente_id):
    # Buscar el último pedido del cliente (ordenado por fecha)
    pedido = (
        Pedido.objects
        .filter(cliente_id=cliente_id)
        .order_by('-fecha')
        .first()
    )

    if not pedido:
        return render(request, 'carrito.html', {'mensaje': '🛒 No hay productos en el carrito'})

    # Obtener el último estado del pedido
    ultimo_estado = pedido.estadopedido_set.order_by('-fecha').first()

    # Obtener detalles del pedido
    detalles = DetallePedido.objects.filter(pedido=pedido)

    # Calcular el total por línea
    for d in detalles:
        d.total_linea = d.cantidad * d.precio_unitario

    # Pasar una bandera para saber si el pedido es editable
    es_editable = ultimo_estado.estado_id == 1 if ultimo_estado else False

    return render(request, 'carrito.html', {
        'pedido': pedido,
        'detalles': detalles,
        'es_editable': es_editable,
        'mensaje': None if es_editable else 'Este pedido ya no se puede modificar.'
    })


@csrf_exempt
def actualizar_entrega(request, pedido_id):
    if request.method == 'POST':
        tipo_entrega = request.POST.get('tipo_entrega')
        direccion = request.POST.get('direccion')
        
        pedido = get_object_or_404(Pedido, pk=pedido_id)
        pedido.tipo_entrega = tipo_entrega
        
        if tipo_entrega == 'domicilio' and direccion:
            pedido.cliente.direccion = direccion
            pedido.cliente.save()
        
        pedido.save()
    return redirect('ver_carrito_html', cliente_id=pedido.cliente_id)

#Sistema interno: Ver detalle de un pedido específico
#Descuenta INVENTARIO si el estado es "Enviado"
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

        # 👇 Descontar stock si el estado es "Enviado o entregado"
        if estado_id == '3' or estado_id == '4':  # Cambia el número si tu estado "Enviado o entregado" tiene otro ID
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

    
#Parte 6 Pendiente!!!!!
from django.contrib.auth.models import User

def detalle_pedido_view(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    detalles = DetallePedido.objects.filter(pedido_id=pedido_id)
    historial = EstadoPedido.objects.filter(pedido_id=pedido_id).order_by('-fecha')
    estados = Estado.objects.all()

     # ✅ Parte 6: Calcular total por detalle
    for d in detalles:
        d.total = d.cantidad * d.precio_unitario  # Agrega el total como atributo temporal

    # Creamos un diccionario con el nombre de cada usuario
    usuarios = {u.id: u.username for u in User.objects.all()}

    # Enlazamos nombre de usuario en cada cambio de estado
    historial_con_nombre = []
    for h in historial:
        nombre_usuario = usuarios.get(h.actor_id, 'Desconocido') if h.actor_tipo == 'usuario' else 'cliente'
        historial_con_nombre.append({
            'estado': h.estado,
            'fecha': h.fecha,
            'actor': nombre_usuario,
            'actor_tipo': h.actor_tipo
        })

    return render(request, 'pagina/detalle_pedido.html', {
        'pedido': pedido,
        'detalles': detalles,
        'historial': historial_con_nombre,
        'estados': estados
    })

def historial_pedidos(request, cliente_id):
    pedidos = Pedido.objects.filter(cliente_id=cliente_id).order_by('-fecha')

    historial = []
    for pedido in pedidos:
        ultimo_estado = EstadoPedido.objects.filter(pedido=pedido).order_by('-fecha').first()
        detalles = DetallePedido.objects.filter(pedido=pedido)

        historial.append({
            'pedido': pedido,
            'estado': ultimo_estado,
            'detalles': detalles
        })

    return render(request, 'historial_pedidos.html', {
        'historial': historial
    })




@csrf_exempt
def seleccionar_pago(request, pedido_id):
    if request.method == 'POST':
        metodo = request.POST.get('metodo_pago')
        pedido = get_object_or_404(Pedido, pk=pedido_id)

        # Guardar o redirigir según el método seleccionado
        if metodo == 'webpay':
            return redirect('iniciar_pago', pedido_id=pedido.pedido_id)
        elif metodo == 'efectivo':
            # Aquí puedes guardar el método y mostrar instrucciones
            return redirect('pago_efectivo', pedido_id=pedido_id)
        elif metodo == 'transferencia':
            return redirect('pago_transferencia', pedido_id=pedido_id)
        else:
            return redirect('ver_carrito_html', cliente_id=pedido.cliente.cliente_id)



def pago_efectivo(request, pedido_id):
    pedido = Pedido.objects.get(pedido_id=pedido_id)

    # Crear el registro de pago
    Pago.objects.create(
        pedido=pedido,
        metodo_pago='Efectivo',
        monto=pedido.total,
        authorization_code=None  # o simplemente omitir si es null
    )

    # Cambiar el estado del pedido a "Pago aprobado"
    EstadoPedido.objects.create(
        pedido=pedido,
        estado_id=7,  # 7 = Pago aprobado
        fecha=datetime.now(),
        actor_id=request.user.cliente.cliente_id,
        actor_tipo='cliente'
    )

    return render(request, 'pagos_app/exito.html', {'pedido': pedido})



@api_view(['GET'])
def pago_transferencia(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)

    # Crear el pago
    Pago.objects.create(
        pedido=pedido,
        metodo_pago='Transferencia',
        monto=pedido.total,
        fecha_pago=now(),
        authorization_code='manual'  # O 'TRANSFER' si quieres otro identificador
    )

    # Registrar nuevo estado: Pago aprobado
    EstadoPedido.objects.create(
        pedido=pedido,
        estado_id=7,  # Pago aprobado
        fecha=now(),
        actor_id=pedido.cliente_id,
        actor_tipo='cliente',
    )

    return render(request, 'pagos_app/transferencia_confirmada.html', {'pedido': pedido})



"""Configuración del logger para registrar eventos

logger = logging.getLogger('django')

def detalle_pedido(request, pedido_id):
    try:
        pedido = get_object_or_404(Pedido, pedido_id=pedido_id)
        logger.info(f'Se accedió al detalle del pedido {pedido_id} por el usuario {request.user.username}')
        return render(request, 'pedidos_app/detalle.html', {'pedido': pedido})
    except Exception as e:
        logger.error(f'Error al cargar el pedido {pedido_id}: {str(e)}')
        return render(request, 'pedidos_app/error.html')"""


