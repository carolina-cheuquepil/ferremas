from django.http import JsonResponse
from inventario_app.models import HistorialInventario
from inventario_app.serializers import HistorialInventarioSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

#Read all
def get_all_inventario(request):
    if request.method == 'GET':
        inventarios = HistorialInventario.objects.all()
        serializer = HistorialInventarioSerializer(inventarios, many=True)
        return JsonResponse(serializer.data, safe=False)
    
#Crear
@api_view(['POST'])
def crear_registro(request):
    serializer = HistorialInventarioSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Update
@api_view(['PUT'])
def actualizar_registro(request, movimiento_id):
    try:
        historial = HistorialInventario.objects.get(pk=movimiento_id)
    except HistorialInventario.DoesNotExist:
        return Response({'error': 'Registro no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    serializer = HistorialInventarioSerializer(historial, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Editar un campo
@api_view(['PATCH'])
def actualizar_registro_parcial(request, movimiento_id):
    try:
        historial = HistorialInventario.objects.get(pk=movimiento_id)
    except HistorialInventario.DoesNotExist:
        return Response({'error': 'Registro no encontrado'}, status=404)

    serializer = HistorialInventarioSerializer(historial, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def eliminar_registro(request, movimiento_id):
    try:
        historial = HistorialInventario.objects.get(pk=movimiento_id)
        historial.delete()
        return Response({'mensaje': 'Registro eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)
    except HistorialInventario.DoesNotExist:
        return Response({'error': 'Registro no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    

