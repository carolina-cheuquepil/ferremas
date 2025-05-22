from django.db import models

class Pago(models.Model):
    pago_id = models.AutoField(primary_key=True)
    pedido = models.ForeignKey('pedidos_app.Pedido', on_delete=models.CASCADE, db_column='pedido_id')
    fecha_pago = models.DateTimeField(auto_now_add=True)
    metodo_pago = models.CharField(max_length=50, null=True, blank=True)
    monto = models.IntegerField()

    class Meta:
        db_table = 'Pago'
        managed = False

    def __str__(self):
        return f"Pago {self.pago_id} - Pedido {self.pedido_id}"

