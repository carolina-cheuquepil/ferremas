from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    usuario_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(max_length=100)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    cargo = models.CharField(max_length=50)
    rut = models.CharField(max_length=20)
    contrasena = models.CharField(max_length=255) 
    #Usuario relacionado con el modelo User de Django
    #user_id porque usuario_id ya era utilizado en la tabla de Usuario
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, db_column='user_id')

    class Meta:
        db_table = 'usuario'
        managed = False  # Tabla en la base de datos

class Cliente(models.Model):
    cliente_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(max_length=100)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    rut = models.CharField(max_length=20)
    contrasena = models.CharField(max_length=255)  # Aquí va el hash
    # Usuario relacionado con el modelo User de Django
    #Para casos donde el cliente se registre en el carrito de compras
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'cliente'
        managed = False  
