from django.db import models

# Create your models here.


class Servidor(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    nombre = models.CharField(max_length=64,null=False)
    ip = models.CharField(max_length=64,null=True)
    puerto = models.IntegerField(null=True)
    motor = models.CharField(max_length=64,null=True)
    descripcion = models.TextField(null=True)
    
    class Meta:
        db_table = 'servidores'   

    def __str__(self):
        return self.nombre


class Base(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    nombre = models.CharField(max_length=64,null=False)
    usuario = models.CharField(max_length=64,null=False)
    contrasenia = models.CharField(max_length=64,null=False)
    descripcion = models.TextField(null=True)
    
    class Meta:
        db_table = 'bases'   

    def __str__(self):
        return self.nombre





        
