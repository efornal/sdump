from django.contrib import admin
from dumpserver.models import Grupo, Servidor, Base, Usuario, Version
from django.forms.widgets import SelectMultiple
from django.db import models

class GrupoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'directorio')
    search_fields = ['nombre','directorio']

class BaseAdmin(admin.ModelAdmin):
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





