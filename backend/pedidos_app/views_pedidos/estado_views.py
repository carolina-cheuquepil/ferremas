from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from pedidos_app.models import Estado
from pedidos_app.serializers import EstadoSerializer

# Obtener todos los estados
@api_view(['GET'])
def listar_estados(request):
    estados = Estado.objects.all()
    serializer = EstadoSerializer(estados, many=True)
    return Response(serializer.data)

# Obtener estado por ID
@api_view(['GET'])
def obtener_estado(request, pk):
    try:
        estado = Estado.objects.get(pk=pk)
        serializer = EstadoSerializer(estado)
        return Response(serializer.data)
    except Estado.DoesNotExist:
        return Response({'error': 'No encontrado'}, status=404)

