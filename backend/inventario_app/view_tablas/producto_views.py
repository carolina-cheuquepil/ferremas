# 4.- JPARepository / ORM Objects: Consulta a BD

from django.http import JsonResponse
from inventario_app.models import Producto
from inventario_app.serializers import ProductoSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

#Read all
def productos_api(request):
    if request.method == 'GET':
        productos = Producto.objects.all()
        serializer = ProductoSerializer(productos, many=True)
        return JsonResponse(serializer.data, safe=False)

#Crear
@api_view(['POST'])
def crear_producto(request):
    serializer = ProductoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Read one
@api_view(['GET'])
def obtener_producto(request, pk):
    try:
        producto = Producto.objects.get(pk=pk)
        serializer = ProductoSerializer(producto)
        return Response(serializer.data)
    except Producto.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
#Update
@api_view(['PUT'])
def actualizar_producto(request, pk):
    try:
        producto = Producto.objects.get(pk=pk)
    except Producto.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductoSerializer(producto, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Delete
@api_view(['DELETE'])
def eliminar_producto(request, pk):
    try:
        producto = Producto.objects.get(pk=pk)
        producto.delete()
        return Response({'mensaje': 'Producto eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)
    except Producto.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

