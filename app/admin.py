# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from app.models import Grupo, Servidor, Base, Usuario, Version
from django.forms.widgets import SelectMultiple
from django.db import models
from django import forms
from django.forms import ModelForm, PasswordInput
from .models import Base
from .models import Share
from django.utils.translation import ugettext as _
from django.utils import translation
from django.contrib import messages
import logging
import sys
import os
from django.conf import settings
import os
import pwd
import grp
import subprocess
from django import forms
from app.forms import ServidorForm


class GrupoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'directorio')
    search_fields = ['nombre','directorio']
    ordering = ('nombre',)
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        grupo = Grupo.objects.get(id = object_id)
        if not grupo.posee_directorio_dumps():
            messages.warning(request,
                             "No pudo verificarse el directorio '%s'" % grupo.dumps_directory_name() )
        return super(GrupoAdmin, self).change_view(request, object_id,'', extra_context)

    
class BaseAdminForm(forms.ModelForm):
    class Meta:
        model = Base
        fields = '__all__'
        widgets = {
            'contrasenia': PasswordInput(render_value=True),
        }

    def clean(self):
        if not self.cleaned_data["contrasenia"] and not self.cleaned_data["password_id"]:
            self.add_error('contrasenia',_('password_or_id_required') )

        
def delete_config_file(file_path):
    try:
        logging.warning("Eliminating file if it exists: '%s'" % file_path)
        os.remove(file_path)
        return True
    except OSError:
        pass
    except Exception as e:
        logging.error("ERROR Exception: %s" % e)
    return False


class BaseAdmin(admin.ModelAdmin):
    form = BaseAdminForm
    list_display = ('nombre', 'servidor', 'grupo', 'password_id',
                    'periodic_dump', 'alow_sharing')
    list_filter = ('servidor','grupo', 'periodic_dump', 'alow_sharing',)
    search_fields = ['nombre','password_id','usuario']

    ordering = ('nombre','servidor','grupo')

    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['db_connection_verification'] = settings.DATABASE_CONNECTION_VERIFICATION
        return super(BaseAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

    
    def save_model(self, request, obj, form, change):

        file_name = "%s_%s.conf" % (obj.servidor,obj.nombre)
        file_path = os.path.join(settings.DUMPS_CONFIG_DIRECTORY,file_name)

        if obj.pk:
            database = Base.objects.get(pk=obj.pk)
            old_file_name = "%s_%s.conf" % (database.servidor,database.nombre)
            old_file_path = os.path.join(settings.DUMPS_CONFIG_DIRECTORY,old_file_name)
            delete_config_file(old_file_path)
            
        delete_config_file(file_path)

        if obj.periodic_dump:
            if obj.servidor.nombre and obj.nombre and \
               obj.usuario and obj.grupo.directorio and obj.password_id:
                try:
                    if not hasattr(settings, 'DUMPS_CONFIG_AUTHENTICATION'):
                        logging.error("Undefined variable DUMPS_CONFIG_AUTHENTICATION, " \
                                      "no configuration file is created")
                        super(BaseAdmin, self).save_model(request, obj, form, change)
                    
                    file_content = ""
                    file_content += "DB_HOST='%s'\n" % obj.servidor.ip
                    file_content += "DB_NAME='%s'\n" % obj.nombre
                    if obj.servidor.motor:
                        file_content += "DB_ENGINE='%s'\n" % obj.servidor.motor
                    if obj.servidor.version:
                        file_content += "DB_ENGINE_VERSION='%s'\n" % obj.servidor.version
                    if obj.servidor.puerto:
                        file_content += "DB_ENGINE_PORT='%s'\n" % obj.servidor.puerto
                    
                    file_content += "DUMPS_PATH='%s'\n" \
                                    % os.path.join( obj.grupo.directorio,
                                                    settings.SUFFIX_PERIODICAL_DUMPS)
                        
                    if 'id' in settings.DUMPS_CONFIG_AUTHENTICATION:
                        file_content += "ID_RATTIC='%s'\n" % obj.password_id

                    if 'username' in settings.DUMPS_CONFIG_AUTHENTICATION:
                        file_content += "DB_USER='%s'\n" % obj.usuario
                        file_content += "DB_PASS='%s'\n" % obj.contrasenia
                        
                    if obj.extra_command_options:
                        file_content += "EXTRA_OPTIONS='%s'\n" % obj.extra_command_options

                    logging.error("Creating configuration file: %s" % file_path)
                    file_hand = open(file_path,'w')
                    file_hand.write(file_content)
                    file_hand.close()
                    subprocess.call("chmod %s %s" % (settings.PERMISSIONS_CONFIG_DUMP_FILE,
                                                     file_path),
                                    shell=True)
                except Exception as e:
                    logging.error("ERROR Exception: %s" % e)
                    messages.error( request, _('msg_backup_config_file_error') % \
                                    {'filename':file_path} )
            else:
                logging.error("Incomplete parameters to create configuration file dump.")
                obj.periodic_dump = False
                messages.warning( request, _('msg_incomplete_parameters') )
                    
        super(BaseAdmin, self).save_model(request, obj, form, change)

    
        
class ServidorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ip', 'puerto', 'motor', 'version')
    search_fields = ['nombre','ip']
    ordering = ('nombre',)
    form = ServidorForm

    
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'usuario')
    search_fields = ['nombre','usuario']
    list_filter = ('grupos',)
    formfield_overrides = { models.ManyToManyField: {'widget': SelectMultiple(attrs={'size':'20'})}, }
    ordering = ('nombre',)

    
class ShareAdmin(admin.ModelAdmin):
   list_display = ('name', 'hash', 'database')
   search_fields = ['name','database']
   ordering = ('name',)

    
admin.site.register(Grupo, GrupoAdmin)
admin.site.register(Base, BaseAdmin)
admin.site.register(Servidor, ServidorAdmin)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Version)
admin.site.register(Share,ShareAdmin)





