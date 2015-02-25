from django.db import models

# Create your models here.


class Grupo(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    nombre = models.CharField(max_length=100,null=False)
    directorio = models.TextField(null=True)
    
    class Meta:
        db_table = 'grupos'   

    def __str__(self):
        return self.nombre

    
class Servidor(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    nombre = models.CharField(max_length=100,null=False)
    ip = models.CharField(max_length=100,null=True)
    puerto = models.IntegerField(null=True)
    motor = models.CharField(max_length=100,null=True)
    descripcion = models.TextField(null=True)
    
    class Meta:
        db_table = 'servidores'
        verbose_name_plural = 'Servidores'
        
    def __str__(self):
        return self.nombre


class Base(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    nombre = models.CharField(max_length=100, null=False)
    usuario = models.CharField(max_length=100, null=False)
    contrasenia = models.CharField(max_length=100, null=False)
    descripcion = models.TextField(null=True)
    servidor = models.ForeignKey(Servidor, null=True)
    grupo = models.ForeignKey(Grupo, null=True)
    
    class Meta:
        db_table = 'bases'   

    def __str__(self):
        return self.nombre


class Usuario(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    nombre  = models.CharField(max_length=100,null=False)
    usuario = models.CharField(max_length=100,null=False)
    grupos = models.ManyToManyField(Grupo)
     
    class Meta:
        db_table = 'usuarios'   

    def __str__(self):
        return self.nombre

