from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from pedidos_app.models import DetallePedido
from pedidos_app.serializers import DetallePedidoSerializer

@api_view(['POST'])
def crear_detalle_pedido(request):
    serializer = DetallePedidoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def listar_detalles_pedido(request):
    detalles = DetallePedido.objects.all()
    serializer = DetallePedidoSerializer(detalles, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def obtener_detalle_pedido(request, pk):
    try:
        detalle = DetallePedido.objects.get(pk=pk)
    except DetallePedido.DoesNotExist:
        return Response({'error': 'Detalle no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    serializer = DetallePedidoSerializer(detalle)
    return Response(serializer.data)


@api_view(['PUT'])
def actualizar_detalle_pedido_put(request, pk):
    try:
        detalle = DetallePedido.objects.get(pk=pk)
    except DetallePedido.DoesNotExist:
        return Response({'error': 'Detalle no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = DetallePedidoSerializer(detalle, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def actualizar_detalle_pedido_patch(request, pk):
    try:
        detalle = DetallePedido.objects.get(pk=pk)
    except DetallePedido.DoesNotExist:
        return Response({'error': 'Detalle no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = DetallePedidoSerializer(detalle, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def eliminar_detalle_pedido(request, pk):
    try:
        detalle = DetallePedido.objects.get(pk=pk)
    except DetallePedido.DoesNotExist:
        return Response({'error': 'Detalle no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    detalle.delete()
    return Response({'mensaje': 'Eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)
