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
            'contrasenia': PasswordInput(),
        }
        
class BaseAdmin(admin.ModelAdmin):
    form = BaseAdminForm
    list_display = ('nombre', 'grupo', 'servidor')
    list_filter = ('servidor','grupo')
        
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





