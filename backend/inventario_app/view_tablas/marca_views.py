#recibe la solicitud y arma la lógica.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from inventario_app.serializers import Marca, MarcaSerializer

@api_view(['GET'])
def all_marcas(request):
    categorias = Marca.objects.all()
    serializer = MarcaSerializer(categorias, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_by_id(request, pk):
    try:
        categoria = Marca.objects.get(pk=pk)
    except Marca.DoesNotExist:
        return Response({'error': 'No encontrada'}, status=status.HTTP_404_NOT_FOUND)

    serializer = MarcaSerializer(categoria)
    return Response(serializer.data)

@api_view(['POST'])
def crear_marca(request):
    serializer = MarcaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)