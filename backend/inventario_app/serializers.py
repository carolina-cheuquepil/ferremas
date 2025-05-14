from rest_framework import serializers
from .models import Producto
from utils.divisas import obtener_valor_dolar

class ProductoSerializer(serializers.ModelSerializer):
    precio_usd = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = ['producto_id', 'nombre_producto', 'precio', 'precio_usd']

    def get_precio_usd(self, obj):
        valor_dolar = obtener_valor_dolar()
        return round(obj.precio / valor_dolar, 2) if valor_dolar > 0 else None
