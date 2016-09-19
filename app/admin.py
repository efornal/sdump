# -*- encoding: utf-8 -*-
from django.contrib import admin
from app.models import Grupo, Servidor, Base, Usuario, Version
from django.forms.widgets import SelectMultiple
from django.db import models
from django import forms
from django.forms import ModelForm, PasswordInput
from .models import Base
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

class GrupoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'directorio')
    search_fields = ['nombre','directorio']

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
    list_display = ('nombre', 'grupo', 'servidor')
    list_filter = ('servidor','grupo')

    
    def save_model(self, request, obj, form, change):

        file_name = "%s_%s.conf" % (obj.servidor,obj.nombre)
        file_path = os.path.join(settings.DUMPS_CONFIG_DIRECTORY,file_name)

        database = Base.objects.get(pk=obj.pk)
        old_file_name = "%s_%s.conf" % (database.servidor,database.nombre)
        old_file_path = os.path.join(settings.DUMPS_CONFIG_DIRECTORY,old_file_name)

        delete_config_file(old_file_path)
        delete_config_file(file_path)

        if obj.periodic_dump:
            if obj.servidor.nombre and obj.nombre and \
               obj.usuario and obj.grupo.directorio and obj.password_id:
                try:
                    file_content = ""
                    file_content += "DB_HOST='%s'\n" % obj.servidor.ip
                    file_content += "DB_NAME='%s'\n" % obj.nombre
                    file_content += "DUMPS_PATH='%s'\n" \
                                    % os.path.join( obj.grupo.directorio,
                                                    settings.SUFFIX_PERIODICAL_DUMPS)
                    file_content += "ID_RATTIC='%s'\n" % obj.password_id

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

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'usuario')
    formfield_overrides = { models.ManyToManyField: {'widget': SelectMultiple(attrs={'size':'20'})}, }

admin.site.register(Grupo, GrupoAdmin)
admin.site.register(Base, BaseAdmin)
admin.site.register(Servidor, ServidorAdmin)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Version)





