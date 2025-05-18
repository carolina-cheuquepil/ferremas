from rest_framework import serializers 
from .models import Producto, Categoria, Marca, Sucursal, HistorialInventario

from utils.divisas import obtener_valor_dolar

#2.- Domain: Capa que muestra solo algunos campos de Entidad/Modelos 
#3.- Mapper: getters, setters, constructores
        
class CategoriaSerializer(serializers.ModelSerializer):  #Model Seria lizer: Mapper
    class Meta:
        model = Categoria
        fields = '__all__'
        #fields = ['categoria_id', 'nombre_categoria']

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    #API Banco Central
    precio_usd = serializers.SerializerMethodField()

    #Para no insertar el nombre la de categoría, sólo el n°
    categoria = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all())
    marca = serializers.PrimaryKeyRelatedField(queryset=Marca.objects.all())


    class Meta:
        model = Producto
        fields = '__all__'

    def get_precio_usd(self, obj):
        try:
            valor_dolar = obtener_valor_dolar()
            return round(obj.precio / valor_dolar, 2) if valor_dolar > 0 else None
        except:
            return None
  
class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = '__all__'

class HistorialInventarioSerializer(serializers.ModelSerializer):
    tipo_movimiento = serializers.ChoiceField(choices=['entrada', 'salida'])

    class Meta:
        model = HistorialInventario
        fields = '__all__'








