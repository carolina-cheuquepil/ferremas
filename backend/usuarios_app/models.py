from django.db import models

class Usuario(models.Model):
    usuario_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(max_length=100)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    cargo = models.CharField(max_length=50)
    rut = models.CharField(max_length=20)

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

    class Meta:
        db_table = 'cliente'
        managed = False  

