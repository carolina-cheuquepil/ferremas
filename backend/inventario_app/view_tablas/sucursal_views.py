from rest_framework.decorators import api_view
from rest_framework.response import Response
from inventario_app.models import Sucursal
from inventario_app.serializers import SucursalSerializer
from rest_framework import status

@api_view(['GET'])
def listar_sucursales(request):
    sucursales = Sucursal.objects.all()
    serializer = SucursalSerializer(sucursales, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def obtener_sucursal(request, pk):
    try:
        sucursal = Sucursal.objects.get(pk=pk)
        serializer = SucursalSerializer(sucursal)
        return Response(serializer.data)
    except Sucursal.DoesNotExist:
        return Response({'error': 'Sucursal no encontrada'}, status=status.HTTP_404_NOT_FOUND)
