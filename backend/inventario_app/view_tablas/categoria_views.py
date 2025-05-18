#recibe la solicitud y arma la lógica.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from inventario_app.serializers import Categoria, CategoriaSerializer

@api_view(['GET'])
def listar_categorias(request):
    categorias = Categoria.objects.all()
    serializer = CategoriaSerializer(categorias, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def obtener_categoria(request, pk):
    try:
        categoria = Categoria.objects.get(pk=pk)
    except Categoria.DoesNotExist:
        return Response({'error': 'No encontrada'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CategoriaSerializer(categoria)
    return Response(serializer.data)