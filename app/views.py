# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
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
from django.core.urlresolvers import reverse


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

        
def describe_file (file_path):
    descrived_file = {}
    try:
        file_size = filesizeformat(os.path.getsize(file_path))
        file_name = os.path.basename(file_path)
        [server,text] = file_name.split('_',1)
        text = text.split('-',1)[1]
        [text,time] = text.partition('.')[0].rsplit('_',1)
        [database,date] = text.rsplit('_',1)
        descrived_file = {'file_path': file_path,
                          'file_name': file_name,
                          'database': database,
                          'server': server,
                          'size': file_size,
                          'date': date,
                          'time': time.replace('-',':'), }
    except Exception as e:
        logging.error('ERROR Exception: with file %s, %s' % (file_path,e))
        
    return descrived_file


def describe_files (files):
    descrived_files = []
    for file_path in files:
        descrived_files.append( describe_file(file_path) )
        
    return descrived_files


def make_backups_lists(group_id=None):
    if group_id is None or not (group_id > 0):
        return [[],[]]

    group = Grupo.objects.get( id=group_id )
    
    sporadics_path = os.path.join( settings.DUMPS_DIRECTORY,
                                   group.directorio,
                                   settings.SUFFIX_SPORADIC_DUMPS )
    periodics_path = os.path.join( settings.DUMPS_DIRECTORY,
                                   group.directorio,
                                   settings.SUFFIX_PERIODICAL_DUMPS )

    sporadics =  describe_files( glob.glob("%s%s" % (sporadics_path,'/*')) )
    periodics =  describe_files( glob.glob("%s%s" % (periodics_path,'/*')) )
    return [sporadics,periodics]


@login_required
def index(request):
    username = request.user.username
    group_id = None
     
    if 'group_id' in request.GET and request.GET['group_id']:
        group_id = request.GET['group_id']
        
    [sporadics,periodics] = make_backups_lists(group_id)
    groups = Grupo.objects.values('id','nombre').filter(usuario__usuario=username)
    
    context = {'groups': groups,
               'backup_notification': settings.USER_NOTIFICATION,
               'sporadics': sporadics,
               'periodics': periodics, }
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
def update_list_backups(request):
    group_id = None
     
    if 'group_id' in request.GET and request.GET['group_id']:
        group_id = request.GET['group_id']
        
    [sporadics,periodics] = make_backups_lists(group_id)

    context = {'sporadics': sporadics,
               'periodics': periodics, }
    return render_to_response('_backups_lists.html', context)


@login_required
def update_databases(request):
    group_id = request.session['group_id']
    databases = None
    if 'server_id' in request.GET and request.GET['server_id']:
        server_id = request.GET['server_id']
        databases = Base.objects.filter(grupo_id=group_id).filter(servidor_id=server_id)

    extra_command_options=None
    context = {'databases': databases,
               'extra_command_options': extra_command_options}
    return render_to_response('_select_databases.html', context)


@login_required
def make_backup(request):
    database_id = int(request.POST['database_id'])
    database = Base.objects.get(pk=database_id)
    server = database.servidor
    server_ip = server.ip
    extra_options = ""
    args = []
    backup_directory = os.path.join( database.grupo.directorio,
                                     settings.SUFFIX_SPORADIC_DUMPS)

    logging.warning("Making backup ,...")

    args.append('sudo')
    args.append(settings.DUMPS_SCRIPT)

    if server.version:
        args.append('-m')
        args.append(server.version.nombre)
        
    if 'opt_inserts' in request.POST and request.POST['opt_inserts']=='true':
        args.append('-i')
        
    if 'opt_clean' in request.POST and request.POST['opt_clean']=='true':
        extra_options += ' --clean '
        
    if 'extra_options' in request.POST:
        extra_options += clean_extra_options(request.POST['extra_options'])

    if extra_options:
        args.append('-o')
        args.append(extra_options)

    args.append('-H')
    args.append(server_ip)

    args.append('-d')
    args.append(database.nombre)

    args.append('-U')
    args.append(database.usuario)

    args.append('-D')
    args.append(backup_directory)

    args_debug = list(args)
    args_debug.append('-P')
    args_debug.append('**********')
    
    args.append('-P')
    args.append(database.contrasenia)


    logging.warning("Running with params: \n %s \n" % (args_debug))
    try:
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        returned_code = p.returncode
    except Exception as e:
        logging.error('ERROR Exception: %s' % e)
        
    if returned_code :
        logging.error("ERROR (%s): %s" % (returned_code,err))
        logging.error("Output: %s" % out)
        message_user = "%s\n %s\n" % (_('backup_with_mistakes'),out)
    else:
        logging.warning("Backup output (%s): %s" % (returned_code,out))
        message_user = _('backup_finished')

    return HttpResponse(message_user, content_type="text/plain")


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


def have_file_permissions( username, filename ):
    databases_allowed = Base.objects.values('nombre') \
                                    .filter(grupo__usuario__usuario=username) \
                                    .distinct()
    permitted = []
    for db in databases_allowed:
        permitted.append(db['nombre'])
        
    file_descriptor = describe_file (filename)

    return (file_descriptor['database'] in permitted)


@login_required
def remove(request):
    message = ""

    if 'filename' in request.GET and request.GET['filename']:
        filename = request.GET['filename']
    else:
        messages.warning(request, _('file_not_indicated'))
        return redirect('index')

    if not have_file_permissions(request.user.username,filename):
        logging.error("El usuario %s no tiene permisos para descargar el archivo %s" \
                      %(request.user.username, filename) )
        messages.warning(request, _('without_permission'))
        return redirect('index')

    logging.warning("Removing file: %s" % filename)
    try:
        os.remove(filename)
        logging.warning("Se elimino el archivo: %s" % filename)
        message = _('deleted_file')
    except OSError as e:
        logging.warning("Error removing file: %s" % filename)
        logging.warning("Error: %s" % e)
        message = _('error_deleting')
        pass

    return HttpResponse(message, content_type="text/plain")    



@login_required
def download(request):
    if 'filename' in request.GET and request.GET['filename']:
        filename = request.GET['filename']
    else:
        messages.warning(request, _('file_not_indicated'))
        return redirect('index')

    if not have_file_permissions(request.user.username,filename):
        logging.error("El usuario %s no tiene permisos para descargar el archivo %s" \
                      %(request.user.username, filename) )
        messages.warning(request, _('without_permission'))
        return redirect('index')
        
    logging.warning("Downloading file: %s" % filename)
        
    response = HttpResponse(open(filename, 'rb'), content_type='application/gzip')
    response['Content-Disposition'] = 'attachment; filename="ejemplo.gz"'
    return response
