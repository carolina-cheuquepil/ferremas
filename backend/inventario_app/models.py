#1.- Entity: Models
#2.- Domain: No exite, porque los modelos son el corazón del dominio
#3.- Mapper: Mapea automáticamente tu modelo

from django.db import models

#Tablas relacionada con productos:

class Categoria(models.Model):
    categoria_id = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'categoria'
        managed = False

    def __str__(self):
        return self.nombre_categoria

class Marca(models.Model):
    marca_id = models.AutoField(primary_key=True)
    nombre_marca = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'marca'
        managed = False

    def __str__(self):
        return self.nombre_marca

class Producto(models.Model):
    producto_id = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, db_column='categoria_id')
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, db_column='marca_id')
    modelo = models.CharField(max_length=100, null=True, blank=True)
    precio = models.IntegerField()
    codigo_sku = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'producto'
        managed = False

    def __str__(self):
        return self.nombre_producto
