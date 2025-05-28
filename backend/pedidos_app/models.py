from django.db import models

#PASO 1: Backend
class Estado(models.Model):
    estado_id = models.AutoField(primary_key=True)
    nombre_estado = models.CharField(max_length=50)

    class Meta:
        db_table = 'Estado'
        managed = False  # Asumes que la tabla ya existe en la base de datos

    def __str__(self):
        return self.nombre_estado

class Pedido(models.Model):
    pedido_id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey('usuarios_app.cliente', on_delete=models.CASCADE, db_column='cliente_id')
    sucursal = models.ForeignKey('inventario_app.Sucursal', on_delete=models.SET_NULL, null=True, db_column='sucursal_id')
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.IntegerField(null=True, blank=True)
    tipo_entrega = models.CharField(max_length=10, choices=[('retiro', 'Retiro'), ('domicilio', 'Domicilio')], default='retiro')
    valor_dolar_usado = models.DecimalField(max_digits=10, decimal_places=2)
    total_usd = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'Pedido'
        managed = False  # Porque la tabla ya existe en la base de datos

    def __str__(self):
        return f"Pedido {self.pedido_id}"

class EstadoPedido(models.Model):
    historial_id = models.AutoField(primary_key=True)
    pedido = models.ForeignKey('Pedido', on_delete=models.SET_NULL, null=True, db_column='pedido_id')
    estado = models.ForeignKey('Estado', on_delete=models.SET_NULL, null=True, db_column='estado_id')
    fecha = models.DateTimeField(null=True, blank=True)
    actor_id = models.IntegerField()
    actor_tipo = models.CharField(max_length=10, choices=[('cliente', 'Cliente'), ('usuario', 'Usuario')])

    class Meta:
        db_table = 'estado_pedido'
        managed = False  # Porque la tabla ya existe

    def __str__(self):
        return f"Historial {self.historial_id}"

class DetallePedido(models.Model):
    detalle_id = models.AutoField(primary_key=True)
    pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE, db_column='pedido_id')
    producto = models.ForeignKey('inventario_app.Producto', on_delete=models.CASCADE, db_column='producto_id')
    cantidad = models.IntegerField()
    precio_unitario = models.IntegerField()

    class Meta:
        db_table = 'detalle_pedido'
        managed = False  # Porque la tabla ya está creada en la base de datos

    def __str__(self):
        return f"Detalle {self.detalle_id} - Pedido {self.pedido_id}"


