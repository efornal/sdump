from django.contrib import admin
from dumpserver.models import Grupo, Servidor, Base, Usuario

class GrupoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'directorio')
    search_fields = ['nombre','directorio']

class BaseAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'grupo', 'servidor')
    list_filter = ('servidor','grupo')

class ServidorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ip', 'puerto', 'motor')

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'usuario')
   # list_filter = ('grupo')

admin.site.register(Grupo, GrupoAdmin)
admin.site.register(Base, BaseAdmin)
admin.site.register(Servidor, ServidorAdmin)
admin.site.register(Usuario, UsuarioAdmin)





