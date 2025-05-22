from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Pago
from .serializers import PagoSerializer

@api_view(['POST'])
def crear_pago(request):
    serializer = PagoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def listar_pagos(request):
    pagos = Pago.objects.all()
    serializer = PagoSerializer(pagos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def obtener_pago_por_id(request, id):
    try:
        pago = Pago.objects.get(pk=id)
    except Pago.DoesNotExist:
        return Response({'error': 'Pago no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    serializer = PagoSerializer(pago)
    return Response(serializer.data)

@api_view(['PUT', 'PATCH'])
def actualizar_pago(request, id):
    try:
        pago = Pago.objects.get(pk=id)
    except Pago.DoesNotExist:
        return Response({'error': 'Pago no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    parcial = request.method == 'PATCH'
    serializer = PagoSerializer(pago, data=request.data, partial=parcial)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def eliminar_pago(request, id):
    try:
        pago = Pago.objects.get(pk=id)
    except Pago.DoesNotExist:
        return Response({'error': 'Pago no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    pago.delete()
    return Response({'mensaje': 'Pago eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)

