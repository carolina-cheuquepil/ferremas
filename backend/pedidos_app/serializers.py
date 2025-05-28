from rest_framework import serializers
from .models import Estado, Pedido, EstadoPedido, DetallePedido

#Paso 2: Backend 

class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = ['estado_id', 'nombre_estado']

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'

class EstadoPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoPedido
        fields = [
            'historial_id',
            'pedido',
            'estado',
            'fecha',
            'actor_id',
            'actor_tipo'
        ]
        #depth = 1  Opcional, para mostrar información completa de relaciones

class DetallePedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallePedido
        fields = [
            'detalle_id',
            'pedido',
            'producto',
            'cantidad',
            'precio_unitario'
        ]
        #depth = 1   Solo para mostrar relaciones completas, no para escritura




