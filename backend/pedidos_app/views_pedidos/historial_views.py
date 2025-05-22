from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from pedidos_app.models import EstadoPedido
from pedidos_app.serializers import EstadoPedidoSerializer

@api_view(['PUT'])
def actualizar_estado_pedido_put(request, pk):
    try:
        historial = EstadoPedido.objects.get(pk=pk)
    except EstadoPedido.DoesNotExist:
        return Response({'error': 'Registro no encontrado'}, status=404)
    
    serializer = EstadoPedidoSerializer(historial, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['PATCH'])
def actualizar_estado_pedido_patch(request, pk):
    try:
        historial = EstadoPedido.objects.get(pk=pk)
    except EstadoPedido.DoesNotExist:
        return Response({'error': 'Registro no encontrado'}, status=404)

    serializer = EstadoPedidoSerializer(historial, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def crear_estado_pedido(request):
    serializer = EstadoPedidoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def listar_estados_pedido(request):
    historial = EstadoPedido.objects.all()
    serializer = EstadoPedidoSerializer(historial, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def obtener_estado_pedido(request, pk):
    try:
        historial = EstadoPedido.objects.get(pk=pk)
    except EstadoPedido.DoesNotExist:
        return Response({'error': 'No encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = EstadoPedidoSerializer(historial)
    return Response(serializer.data)


@api_view(['DELETE'])
def eliminar_estado_pedido(request, pk):
    try:
        historial = EstadoPedido.objects.get(pk=pk)
    except EstadoPedido.DoesNotExist:
        return Response({'error': 'No encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    historial.delete()
    return Response({'mensaje': 'Eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)

