# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.dispatch import receiver
import logging
from django.db.models.signals import post_save
from django.conf import settings
from django.utils.translation import ugettext as _
import os
import pwd
import grp
import json
import requests


class RatticAPI(object):
    VERSION = 'v1'
    
    def __init__(self, server=None, creds=None):
        if server is not None:
            self.server = server
        if creds is not None:
            self.creds = creds

    def _headers(self):
        '''Retorna headers requeridos para interactuar con la API de rattic'''
        try:
            return {
                'Authorization': 'ApiKey {}:{}'.format(*self.creds),
                'Accept': 'application/json',
            }
        except Exception as e:            
            logging.error(e)

    def _request(self, key):
        '''Efectúa la petición a la API y devuelve un objeto dict con
        la respuesta obtenida'''
        try:
            result = dict()

            url = "{}/api/{}/cred/{}/?format=json" \
              .format( self.server.rstrip('/'), self.VERSION, key )
              
            response = requests.get( url, headers=self._headers())
            if response.status_code == 200:
                return dict(filter(lambda item: item[0] in ['username','password'],
                                       response.json().items()))
            else:
                logging.error('The request to the rati api could not be made. The http response code was: {}'.format(response.status_code))
        except HTTPError as http_err:
            logging.error('HTTP error occurred: {}'.format(http_err)) 
        except Exception as e:
            logging.eror(e)
        return result

    def get(self, id):
        return self._request(id)
    
    def get_creds(self, id):
        result = self._request(id)
        if bool(result):
            return [v for k,v in result.items()]
        else:
            return ['','']



class Version(models.Model):
    id = models.AutoField(
        primary_key=True,
        null=False)
    nombre = models.CharField(
        max_length=100,
        null=False,
        verbose_name=_('name'))

    
    class Meta:
        db_table = 'versiones'   
        verbose_name = _('Version')
        verbose_name_plural = _('Versions')
        ordering = ['nombre']
        
    def __unicode__(self):
        return self.nombre

    

class Grupo(models.Model):
    id = models.AutoField(
        primary_key=True,
        null=False)
    nombre = models.CharField(
        max_length=100,
        null=False,
        verbose_name=_('name'))
    directorio = models.CharField(
        max_length=255,
        null=True,
        verbose_name=_('directory'))

    
    class Meta:
        db_table = 'grupos'
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')
        ordering = ['nombre']
        
    def __unicode__(self):
        return self.nombre

    
    def dumps_directory_name(self):
        return "%s/%s" % ( settings.DUMPS_DIRECTORY, self.directorio.lower().replace(" ", "_") )

    
    def posee_directorio_dumps(self):
        import os
        return os.path.exists(self.dumps_directory_name())

    
    @classmethod
    def make_dir(cls,path):
        try:
            os.umask(0);
            os.mkdir(path, int(settings.PERMISSIONS_DUMPS_DIRECTORY))
            gid = grp.getgrnam(settings.GROUP_DUMPS_DIRECTORY).gr_gid
            uid = pwd.getpwnam(settings.USER_DUMPS_DIRECTORY).pw_uid
            os.chown(path, uid, gid)
        except OSError as e:
            if e.errno == 17:
                logging.warning("Directory '%s' already exists" % path )
                pass
            else:
                logging.error(e)


    
class Servidor(models.Model):
    id = models.AutoField(
        primary_key=True,
        null=False)
    nombre = models.CharField(
        max_length=100,
        null=False,
        verbose_name=_('name'))
    ip = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_('ip_address'))
    puerto = models.IntegerField(
        null=False,
        verbose_name=_('port'))
    motor = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_('engine'))
    descripcion = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('description'))
    version = models.ForeignKey(
        Version,
        null=True,
        blank=True,
        verbose_name=_('version'))

    
    class Meta:
        db_table = 'servidores'
        verbose_name = _('Server')
        verbose_name_plural = _('Servers')
        ordering = ['nombre']
        
    def __unicode__(self):
        return self.nombre

    

class Base(models.Model):
    id = models.AutoField(
        primary_key=True,
        null=False)
    nombre = models.CharField(
        max_length=100,
        null=False,
        verbose_name=_('name'))
    usuario = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_('username'))
    contrasenia = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_('password'))
    descripcion = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('description'))
    servidor = models.ForeignKey(
        Servidor,
        null=True,
        blank=True,
        verbose_name=_('server'))
    grupo = models.ForeignKey(
        Grupo,
        null=True,
        blank=True,
        verbose_name=_('group'))
    extra_command_options = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
        verbose_name=_('extra_command_options'))
    password_id = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_('password_id'))
    periodic_dump = models.BooleanField(
        default=False,
        verbose_name=_('periodic_dump'))
    last_date_download = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('last_date_download') )
    alow_sharing = models.BooleanField(
        default=False,
        verbose_name=_('alow_sharing'))

    
    class Meta:
        db_table = 'bases'
        verbose_name = _('Database')
        verbose_name_plural = _('Databases')
        ordering = ['nombre']
        
    def __unicode__(self):
        return self.nombre

    

class Usuario(models.Model):
    id = models.AutoField(
        primary_key=True,
        null=False)
    nombre  = models.CharField(
        max_length=100,
        null=False,
        verbose_name=_('name'))
    usuario = models.CharField(
        max_length=100,
        null=False,
        unique=True,
        verbose_name=_('username'))
    grupos = models.ManyToManyField(
        Grupo,
        verbose_name=_('group'))

    
    class Meta:
        db_table = 'usuarios'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['nombre']
        
    def grupos_asignados(self):
        grupos = []
        for grupo in self.grupos.all():
          grupos.append(grupo.nombre)
#          print grupo.nombre
        return ', '.join(grupos)

    
    def __unicode__(self):
        return self.nombre


class Share(models.Model):
    id = models.AutoField(
        primary_key=True,
        null=False)
    database = models.ForeignKey(
        Base,
        null=False,
        verbose_name=_('database'))
    name = models.CharField(
        max_length=254,
        null=False,
        verbose_name=_('name'))
    hash = models.CharField(
        max_length=254,
        null=False,
        verbose_name=_('hash'))

    
    class Meta:
        db_table = 'shares'
        verbose_name = _('Share')
        verbose_name_plural = _('Shares')
        ordering = ['name']
        
    def __unicode__(self):
        return self.name

    
@receiver(post_save, sender=Grupo)
def create_backup_directories (sender, instance, *args, **kwargs):
    dirname = instance.dumps_directory_name()
    logging.info("Creando directorio de backup'%s'" % dirname )
    Grupo.make_dir('%s' % dirname )
    Grupo.make_dir('%s/%s' % (dirname, settings.SUFFIX_SPORADIC_DUMPS) )
    Grupo.make_dir('%s/%s' % (dirname, settings.SUFFIX_PERIODICAL_DUMPS) )
    
