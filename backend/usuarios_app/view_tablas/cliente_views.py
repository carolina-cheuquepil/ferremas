from django.shortcuts import render
import bcrypt #Contraseña hasheada

from rest_framework.views import APIView
from rest_framework.response import Response

from usuarios_app.models import Cliente
from usuarios_app.serializers import ClienteSerializer


from rest_framework.decorators import api_view
from rest_framework import status

#Endpoints CRUD básicos
#Read all
class ClienteListView(APIView):
    def get(self, request):
        clientes = Cliente.objects.all()
        serializer = ClienteSerializer(clientes, many=True)
        return Response(serializer.data)
    
#Create: Incluye hashing de contraseña
@api_view(['POST'])
def crear_cliente(request):
    data = request.data.copy()  # Hacemos una copia editable

    # Hashear la contraseña
    if 'contrasena' in data:
        hashed = bcrypt.hashpw(data['contrasena'].encode('utf-8'), bcrypt.gensalt())
        data['contrasena'] = hashed.decode('utf-8')  # Guardar como string

    serializer = ClienteSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Read by ID
@api_view(['GET'])
def obtener_cliente_por_id(request, cliente_id):
    try:
        cliente = Cliente.objects.get(pk=cliente_id)
    except Cliente.DoesNotExist:
        return Response({'error': 'Cliente no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ClienteSerializer(cliente)
    return Response(serializer.data)

#Update
@api_view(['PUT', 'PATCH'])
def actualizar_cliente(request, cliente_id):
    try:
        cliente = Cliente.objects.get(pk=cliente_id)
    except Cliente.DoesNotExist:
        return Response({'error': 'Cliente no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    # partial=True permite actualizar campos específicos si es PATCH
    serializer = ClienteSerializer(cliente, data=request.data, partial=(request.method == 'PATCH'))

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Delete
@api_view(['DELETE'])
def eliminar_cliente(request, cliente_id):
    try:
        cliente = Cliente.objects.get(pk=cliente_id)
    except Cliente.DoesNotExist:
        return Response({'error': 'Cliente no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    cliente.delete()
    return Response({'mensaje': 'Cliente eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def login_cliente(request):
    correo = request.data.get('correo')
    contrasena = request.data.get('contrasena')

    try:
        cliente = Cliente.objects.get(correo=correo)
    except Cliente.DoesNotExist:
        return Response({'error': 'Correo no registrado'}, status=status.HTTP_404_NOT_FOUND)

    if bcrypt.checkpw(contrasena.encode('utf-8'), cliente.contrasena.encode('utf-8')):
        return Response({'mensaje': 'Login exitoso', 'cliente_id': cliente.cliente_id})
    else:
        return Response({'error': 'Contraseña incorrecta'}, status=status.HTTP_401_UNAUTHORIZED)

