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
import os
import glob
from django.template.defaultfilters import filesizeformat
import subprocess
from django.contrib import messages

@login_required
def index(request):
    request.session['group_id'] = None
    username = request.user.username
#    groups = Grupo.objects.values('id','nombre').filter(usuario__usuario=username)
    groups = Grupo.objects.all().values('id','nombre') # FIXME ,no usar esta
    context = {'groups': groups, 'user_notification': settings.USER_NOTIFICATION}
    return render(request, 'index.html', context)


@login_required
def update_servers(request):
    group_id = request.GET['group_id']
    request.session['group_id'] = group_id
    servers = Servidor.objects.values('id','nombre'). \
              filter(base__grupo_id=group_id).annotate(cantidad=Count('nombre'))
    context = {'servers': servers,}
    return render_to_response('_select_servers.html', context)


def describe_files (files):
    descrived_files = []
    for filename in files:
        file_size = filesizeformat(os.path.getsize(filename))
        name = os.path.basename(filename)
        [server,text] = name.split('_base-')
        [text,time] = text.partition('.')[0].rsplit('_',1)
        [database,date] = text.rsplit('_',1)
        descrived_files.append( {'filename': filename,
                                 'database': database,
                                 'server': server,
                                 'size': file_size,
                                 'date': date,
                                 'time': time.replace('-',':'), })
    return descrived_files


@login_required
def update_list_backups(request):
    group = Grupo.objects.get( id=request.GET['group_id'] )
    sporadics_path = os.path.join( settings.DUMPS_DIRECTORY,
                                   group.directorio,
                                   settings.SUFFIX_SPORADIC_DUMPS )
    periodics_path = os.path.join( settings.DUMPS_DIRECTORY,
                                   group.directorio,
                                   settings.SUFFIX_PERIODICAL_DUMPS )

    sporadics =  describe_files( glob.glob("%s%s" % (sporadics_path,'/*')) )
    periodics =  describe_files( glob.glob("%s%s" % (periodics_path,'/*')) )
    
    context = {'sporadics': sporadics,
               'periodics': periodics, }
    return render_to_response('_backups_lists.html', context)


@login_required
def update_databases(request):
    group_id = request.session['group_id']
    server_id = request.GET['server_id']
    databases = Base.objects.filter(grupo_id=group_id).filter(servidor_id=server_id)
    extra_command_options= "ejemplo extra"
    context = {'databases': databases,
               'extra_command_options': extra_command_options}
    return render_to_response('_select_databases.html', context)


def clean_extra_options(options):
    cleaned = options
    cleaned.replace('#','')
    cleaned.replace('&','')
    cleaned.replace(';','')
    cleaned.replace('$','')
    cleaned.replace('/','')
    cleaned.replace('<','')
    cleaned.replace('>','')
    return cleaned


@login_required
def make_backup(request):
    group_id = int(request.POST['group_select'])
    server_id = int(request.POST['server_select'])
    database_id = int(request.POST['database_select'])
    database = Base.objects.get(pk=database_id)
    server = database.servidor
    server_ip = server.ip
    extra_options = ""
    
    logging.warning("haciendo backup,...")
    
    if server.version:
        extra_options += " -m %s " % server.version
    if 'opt_inserts' in request.POST:
        extra_options += " --inserts "
    if 'opt_clena' in request.POST:
        extra_options += " --clean "
    if 'extra_options' in request.POST:
        extra_options += clean_extra_options(request.POST['extra_options'])

        
    params = " -H %s %s %s " % ( server_ip,
                               extra_options,
                               settings.DUMPS_DIRECTORY )
    
    p = subprocess.Popen([settings.DUMPS_SCRIPT,params],
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE)
    out, err =  p.communicate()

    logging.warning("Ejecuntando: \n %s %s \n" % (settings.DUMPS_SCRIPT,params))
    logging.error("ERROR: %s" % err)

    messages.add_message(request, messages.SUCCESS, out)
    
    return redirect('index')


@login_required
def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
def update_extra_options(request):
    extra_options=""
    if ('database_id' in request.GET) and (request.GET['database_id'] > 0):
        database = Base.objects.get(pk=int(request.GET['database_id']))
        if database.extra_command_options:
            extra_options = database.extra_command_options
    return HttpResponse(extra_options, content_type="text/plain")


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
