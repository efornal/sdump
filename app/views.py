# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import logging
from django.conf import settings
from django.utils.translation import ugettext as _
from django.utils import translation
from .models import Grupo, Servidor, Base
from django.shortcuts import render_to_response
from django.db.models import Count
# Create your views here.

@login_required
def index(request):
    request.session['group_id'] = None
    username = request.user.username
#    groups = Grupo.objects.values('id','nombre').filter(usuario__usuario=username)
    groups = Grupo.objects.all().values('id','nombre')
    context = {'groups': groups}
    return render(request, 'index.html', context)


@login_required
def update_servers(request):
    group_id = request.GET['group_id']
    request.session['group_id'] = group_id
    servers = Servidor.objects.values('id','nombre'). \
              filter(base__grupo_id=group_id).annotate(cantidad=Count('nombre'))
    context = {'servers': servers,}
    return render_to_response('_select_servers.html', context)


@login_required
def update_databases(request):
    group_id = request.session['group_id']
    server_id = request.GET['server_id']
    databases = Base.objects.filter(grupo_id=group_id).filter(servidor_id=server_id)
    context = {'databases': databases,}
    return render_to_response('_select_databases.html', context)


    
@login_required
def logout_view(request):
    logout(request)
    return redirect('index')


def login_view(request):
    if request.POST.get('username') and request.POST.get('password'):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('index')
            else:
                return render(request, 'login.html')
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')
