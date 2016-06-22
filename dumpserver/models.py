# -*- encoding: utf-8 -*-
from django.db import models
from django.dispatch import receiver
import logging
from django.db.models.signals import post_save
from django.conf import settings



class Version(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    nombre = models.CharField(max_length=100,null=False)
    
    class Meta:
        db_table = 'versiones'   
        verbose_name_plural = 'Versiones'

    def __unicode__(self):
        return self.nombre


class Grupo(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    nombre = models.CharField(max_length=100,null=False)
    directorio = models.CharField(max_length=255,null=True)
    
    class Meta:
        db_table = 'grupos'   
        verbose_name_plural = 'Grupos'

    def __unicode__(self):
        return self.nombre

    def dumps_directory_name(self):
        return "%s/%s" % ( settings.DUMPS_DIRECTORY, self.directorio.lower().replace(" ", "_") )

    def posee_directorio_dumps(self):
        import os
        return os.path.exists(self.dumps_directory_name())
    
    @classmethod
    def make_dir(cls,path):
        import os
        import pwd
        import grp
        try:
            os.umask(0);
            os.mkdir(path, settings.PERMISSIONS_DUMPS_DIRECTORY)
            gid = grp.getgrnam(settings.GROUP_DUMPS_DIRECTORY).gr_gid
            uid = pwd.getpwnam(settings.USER_DUMPS_DIRECTORY).pw_uid
            os.chown(path, uid, gid)
        except OSError as e:
            if e.errno == 17:
                logging.warning("Directory '%s' already exists" % path )
                pass
            else:
                logging.error(e)

                
@receiver(post_save, sender=Grupo)
def create_backup_directories (sender, instance, *args, **kwargs):
    dirname = instance.dumps_directory_name()
    logging.info("Creando directorio de backup'%s'" % dirname )
    Grupo.make_dir('%s' % dirname )
    Grupo.make_dir('%s/%s' % (dirname, settings.SUFFIX_SPORADIC_DUMPS) )
    Grupo.make_dir('%s/%s' % (dirname, settings.SUFFIX_PERIODICAL_DUMPS) )

    
class Servidor(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    nombre = models.CharField(max_length=100,null=False)
    ip = models.CharField(max_length=100,null=True, blank=True)
    puerto = models.IntegerField(null=True, blank=True)
    motor = models.CharField(max_length=100,null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    version = models.ForeignKey(Version, null=True, blank=True)
        
    class Meta:
        db_table = 'servidores'
        verbose_name_plural = 'Servidores'

    def __unicode__(self):
        return self.nombre
    

class Base(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    nombre = models.CharField(max_length=100, null=False)
    usuario = models.CharField(max_length=100, null=False)
    contrasenia = models.CharField(max_length=100, null=False)
    descripcion = models.TextField(null=True, blank=True)
    servidor = models.ForeignKey(Servidor, null=True, blank=True)
    grupo = models.ForeignKey(Grupo, null=True, blank=True)
    
    class Meta:
        db_table = 'bases'
        verbose_name_plural = 'Bases'

    def __unicode__(self):
        return self.nombre


class Usuario(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    nombre  = models.CharField(max_length=100,null=False)
    usuario = models.CharField(max_length=100,null=False, unique=True)
    grupos = models.ManyToManyField(Grupo)
     
    class Meta:
        db_table = 'usuarios'
        verbose_name_plural = 'Usuarios'

    def grupos_asignados(self):
        grupos = []
        for grupo in self.grupos.all():
          grupos.append(grupo.nombre)
          print grupo.nombre
        return ', '.join(grupos)

    def __unicode__(self):
        return self.nombre
