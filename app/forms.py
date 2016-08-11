# -*- encoding: utf-8 -*-
from django import forms
from django.forms import ModelForm, PasswordInput
from .models import Base
from django.utils.translation import ugettext as _
from django.utils import translation

class BaseForm(forms.ModelForm):
    nombre = forms.CharField(max_length=100, required=True, label=_('nombre'))
    usuario = forms.CharField(max_length=100, required=True, label=_('usuario'))
    contrasenia = forms.CharField(max_length=100, required=True, label=_('contrasenia') )
    descripcion = forms.TextField(required=False, label=_('descripcion'))
    servidor = forms.ForeignKey(Servidor, required=False, label=_('servidor'))
    grupo = forms.ForeignKey(Grupo, required=False, label=_('grupo'))
    
    class Meta:
        model = Base
        fields = ('nombre', 'usuario', 'contrasenia', 'descripcion', 'servidor', 'grupo_id')
