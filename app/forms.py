# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.forms import ModelForm, PasswordInput
from .models import Base, Servidor
from django.utils.translation import ugettext as _
from django.utils import translation
from django.conf import settings
from django.forms import ModelForm
from django.forms import Textarea


class BaseForm(forms.ModelForm):
    nombre = forms.CharField(max_length=100, required=True, label=_('nombre'))
    usuario = forms.CharField(max_length=100, required=True, label=_('usuario'))
    contrasenia = forms.CharField(max_length=100, required=True, label=_('contrasenia') )
    descripcion = forms.CharField(required=False, widget=forms.Textarea, label=_('description'))

    class Meta:
        model = Base
        fields = ('nombre', 'usuario', 'contrasenia', 'descripcion',)


class ServidorForm(forms.ModelForm):
    nombre = forms.CharField(max_length=100,required=True, label=_('name'))
    ip = forms.CharField(max_length=100,required=False, label=_('ip_address'))
    puerto = forms.IntegerField(required=False, label=_('port'))
    motor = forms.ChoiceField( choices = settings.ENGINE_OPTIONS)
    descripcion = forms.CharField(required=False, widget=forms.Textarea, label=_('description'))


    class Meta:
        model = Servidor
        fields = ('nombre', 'ip', 'puerto', 'motor', 'descripcion', 'version')
