from django.db import models

# Create your models here.

class Version(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    nombre = models.CharField(max_length=100,null=False)

    
    class Meta:
        db_table = 'versiones'   
        verbose_name_plural = 'Versiones'
        
    def __str__(self):
        return self.nombre

class Grupo(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    nombre = models.CharField(max_length=100,null=False)
    directorio = models.TextField(null=True)
    
    class Meta:
        db_table = 'grupos'   
        verbose_name_plural = 'Grupos'
        
    def __str__(self):
        return self.nombre

    
class Servidor(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    nombre = models.CharField(max_length=100,null=False)
    ip = models.CharField(max_length=100,null=True)
    puerto = models.IntegerField(null=True)
    motor = models.CharField(max_length=100,null=True)
    descripcion = models.TextField(null=True)
    version = models.ForeignKey(Version, null=True)
        
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
        verbose_name_plural = 'Bases'

    def __str__(self):
        return self.nombre


class Usuario(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    nombre  = models.CharField(max_length=100,null=False)
    usuario = models.CharField(max_length=100,null=False)
    grupos = models.ManyToManyField(Grupo)
     
    class Meta:
        db_table = 'usuarios'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.nombre

    def grupos_asignados(self):
        grupos = []
        for grupo in self.grupos.all():
          grupos.append(grupo.nombre)
          print grupo.nombre
        return ', '.join(grupos)

