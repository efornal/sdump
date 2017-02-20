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
import datetime
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
import re
import os
from wsgiref.util import FileWrapper
from django.http import FileResponse
from django import forms
import json
from decorators import validate_basic_http_autorization, validate_https_request

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


def number_of_backups(path):
    try:
        logging.error("dir count backup: %s" % path)
        return len( glob.glob("%s" % path) )
    except Exception as e:
        logging.error ("ERROR Exception: Number of backups for '%s'. %s" % (path,e))
        pass
    return None


def to_date_according_to_text(s_date):
    date_patterns = ["%d-%m-%Y", "%Y-%m-%d"]

    for pattern in date_patterns:
        try:
            return datetime.datetime.strptime(s_date, pattern).date()
        except:
            pass

    return None


def describe_file (file_path):

    descrived_file = {}
    try:
        file_size = filesizeformat(os.path.getsize(file_path))
        file_name = os.path.basename(file_path)
        [server,text] = re.split("_base-|_base_con_historico-|_base_sin_hist-",file_name)
        [database,date,time,text] = re.split("_([0-9]{2,4}-[0-9]{2}-[0-9]{2,4})[_|-]([0-9]{2}[-|_][0-9]{2})",text)
        time = time.replace('_',':').replace('-',':')
        fdate = to_date_according_to_text(date)
        date = fdate.strftime("%d-%m-%Y")
        descrived_file = {'file_path': file_path,
                          'file_name': file_name,
                          'database': database,
                          'server': server,
                          'size': file_size,
                          'date': date,
                          'time': time, }
    except Exception as e:
        logging.error('ERROR Exception: with file %s, %s' % (file_path,e))
        
    return descrived_file


def describe_files (files):
    descrived_files = []
    for file_path in files:
        descrived_files.append( describe_file(file_path) )
        
    return descrived_files


def make_backups_lists(group_id=None):
    backups_lists = [[],[]]

    if group_id is None or not (int(group_id) > 0):
        return backups_lists

    try:
        group = Grupo.objects.get( id=group_id )
        
        sporadics_path = os.path.join( settings.DUMPS_DIRECTORY,
                                       group.directorio,
                                       settings.SUFFIX_SPORADIC_DUMPS )
        periodics_path = os.path.join( settings.DUMPS_DIRECTORY,
                                       group.directorio,
                                       settings.SUFFIX_PERIODICAL_DUMPS )

        sporadics =  describe_files( sorted(glob.glob("%s%s" % (sporadics_path,'/*')),
                                            reverse=True) )
        periodics =  describe_files( sorted(glob.glob("%s%s" % (periodics_path,'/*')),
                                            reverse=True) )
        backups_lists = [sporadics,periodics]
    except Exception as e:
        logging.error('ERROR Exception: with group_id %s, %s' % (group_id,e))

    return backups_lists


def ip_from_vm_name( vm_name='' ):
    args = ['host',"{}".format(vm_name)]
    try:
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        ip_reg = re.search('[0-9]+.[0-9]+.[0-9]+.[0-9]+', out)
        if ip_reg:
            return ip_reg.group(0)
        else:
            return ''
        
    except Exception as e:
        logging.error('ERROR Exception: %s' % e)
        return ''

    
def get_rattic_pass( rattic_id ):
    params = ['sudo',settings.RATTIC_KEY_RETRIEVAL_SCRIPT,'-u', '-c', '-i', unicode(rattic_id)]

    logging.info("Getting for rattic id: {}".format(rattic_id))
    try:
        p = subprocess.Popen(params, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        
        if out:
            return out.split('\n')[0:2]
        else:
            return ''
    
    except Exception as e:
        logging.error('ERROR Exception: %s' % e)
        return ''

    
def pg_check( args={} ):
    pg_env = os.environ.copy()
    pg_env["PGPASSWORD"] = args["db_pass"]
    params = ['psql',"-U",args["db_user"],
              "-d",args["db_name"],
              "-h",args["db_server"],
              "-p",args["db_port"],
              "-c","select 'test_for_connection'"]
    logging.info("Checking with params: {}".format(params))
    try:
        p = subprocess.Popen(params, env=pg_env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        found = re.search('test_for_connection', out)
        if found:
            return 1
        else:
            return 0
        
    except Exception as e:
        logging.error('ERROR Exception: %s' % e)
        return 0

    
@login_required    
def check_server(request):
    result = {}
    if 'vm_name' in request.POST and request.POST['vm_name']:
        vm_name = request.POST['vm_name']
        logging.info("searching vm name: {}".format(vm_name))

        result.update({'vm_ip': ip_from_vm_name(vm_name)})
    result_list = json.dumps(result)
    return HttpResponse(result_list)


@login_required    
def check_pass(request):
    result = {}
    args={}

    if 'db_name' in request.POST and \
       'db_server' in request.POST:

        server = Servidor.objects.get(nombre=request.POST['db_server'])
        if server:
            args.update({'db_port': unicode(server.puerto)})
        else:
            args.update({'db_port': '5432'})

        if 'db_pass_id' in request.POST and request.POST['db_pass_id']:
            db_user, db_pass = get_rattic_pass(request.POST['db_pass_id'])
            args.update({'db_user': db_user})
            args.update({'db_pass': db_pass})

        if 'db_pass' in request.POST and request.POST['db_pass']:
            args.update({'db_user': request.POST['db_user']})
            args.update({'db_pass': request.POST['db_pass']})

        args.update({'db_name': request.POST['db_name']})
        args.update({'db_server': request.POST['db_server']})

        res = pg_check(args)
        result.update({'result': res})
    else:
        result.update({'result': 0})
        
    result_list = json.dumps(result)
    return HttpResponse(result_list)


@login_required
def index(request,group_id=0, server_id=0, database_id=0):
 
    username = request.user.username
    context={}
        
    if 'group_id' in request.GET and request.GET['group_id']:
        group_id = request.GET['group_id']
        
    [sporadics,periodics] = make_backups_lists(group_id)
    groups = Grupo.objects.values('id','nombre') \
                          .filter(usuario__usuario=username) \
                          .order_by('nombre')
    if group_id:
        servers = Servidor.objects.values('id','nombre') \
                                  .filter(base__grupo_id=group_id) \
                                  .annotate(cantidad=Count('nombre')) \
                                  .order_by('nombre')
        context.update({'servers': servers})

    if group_id and server_id:
        databases = Base.objects.values('id','nombre') \
                                .filter(grupo_id=group_id) \
                                .filter(servidor_id=server_id) \
                                .order_by('nombre')
        context.update({'databases': databases})

    context.update({'group_id': int(group_id),
                    'server_id': int(server_id),
                    'database_id': int(database_id)})
    context.update({'groups': groups})
    context.update({'sporadics': sporadics })
    context.update({'periodics': periodics })
    
    if not group_id:
        context.update({'backup_notification': settings.USER_NOTIFICATION})
    return render(request, 'index.html', context)

    
@login_required
def update_servers(request):
    group_id = request.GET['group_id']
    request.session['group_id'] = group_id
    servers = Servidor.objects.values('id','nombre') \
                              .filter(base__grupo_id=group_id) \
                              .annotate(cantidad=Count('nombre')) \
                              .order_by('nombre')

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
        databases = Base.objects.values('id','nombre') \
                                .filter(grupo_id=group_id) \
                                .filter(servidor_id=server_id) \
                                .order_by('nombre')

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

    # check for maximum sporadick backups
    max_sporadic = 5
    project_backup_dir = os.path.join(settings.DUMPS_DIRECTORY,
                                      backup_directory,                                      
                                      '%s*_base-%s_*' % (database.servidor.ip,
                                                        database.nombre) )
    if hasattr(settings, 'MAX_SPORADICS_BACKUPS'):
        max_sporadic = settings.MAX_SPORADICS_BACKUPS

    number_backups = number_of_backups(project_backup_dir)

    if not (number_backups is None) and (number_backups >= max_sporadic):
        logging.warning("Number of backups (%s) exceeded, the current limit is: %s." % \
                        (number_backups,max_sporadic) )
        message_user = _('number_backups_exceeded') % {'max_copies':max_sporadic}
        return HttpResponse(message_user, content_type="text/plain")

    
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
def update_extra_options(request):
    extra_options=""
    if ('database_id' in request.GET) and (request.GET['database_id'] > 0):
        database = Base.objects.get(pk=int(request.GET['database_id']))
        if database.extra_command_options:
            extra_options = database.extra_command_options
    return HttpResponse(extra_options, content_type="text/plain")




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

    try:
        file_descriptor = describe_file(filename)
        base =  Base.objects.filter(nombre=file_descriptor['database']) \
                            .filter(servidor__ip=file_descriptor['server'])
        if len(base) == 1:
            base = base.first()
            base.last_date_download = datetime.datetime.now()
            base.save(update_fields=['last_date_download'])
    except Exception as e:
        logging.error ("ERROR Exception: Marking download date. %s" % (e))
        pass
                
    logging.warning("Downloading file: %s" % filename)
    attachment_name = os.path.basename(filename)
    response = FileResponse(FileWrapper(file(filename, 'rb')),
                            content_type='application/application/gzip')
    response['Content-Disposition'] = 'attachment; filename="%s"' % attachment_name
    return response


def basic_http_authentication(request):
    import base64
    from django.contrib.auth import authenticate
    auth = request.META['HTTP_AUTHORIZATION'].split()
    user = None
    if len(auth) == 2:
        if auth[0].lower() == "basic":
            uname, passwd = base64.b64decode(auth[1]).split(':')
            user = authenticate(username=uname, password=passwd)
    return user

    
@validate_basic_http_autorization
@validate_https_request
def api_make_backup(request):

    user = basic_http_authentication(request)
    if user is None:
        logging.error("Invalid username or password")
        return HttpResponse('401 Unauthorized', status=401)

    logging.info("Validated user: {}".format(user.username))
    logging.info("Validated user: {}".format(user.username))
    database=None
    try:
        if 'database_id' in request.GET:
            database_id = int(request.GET['database_id'])
            database = Base.objects.get(pk=database_id)
    except Exception as e:
        logging.error ("ERROR Exception: Marking backup. Incorrect database_id. %s" % (e))

    if not database:
        logging.error("Invalid Database Id")
        return HttpResponse('404 Request not found', status=404)
    
    server = database.servidor
    server_ip = server.ip
    extra_options = ""
    args = []
    backup_directory = os.path.join( database.grupo.directorio,
                                     settings.SUFFIX_SPORADIC_DUMPS)

    dump_date=datetime.datetime.now().strftime('%d-%m-%Y_%H-%M')
    backup_name = os.path.join(settings.DUMPS_DIRECTORY,
                               backup_directory,
                               '%s_base-%s_%s.sql.gz' % (database.servidor.ip,
                                                         database.nombre,
                                                         dump_date) )

    # check for maximum sporadick backups
    max_sporadic = 5
    project_backup_dir = os.path.join(settings.DUMPS_DIRECTORY,
                                      backup_directory,
                                      '%s*_base-%s_*' % (database.servidor.ip,
                                                        database.nombre) )
    if hasattr(settings, 'MAX_SPORADICS_BACKUPS'):
        max_sporadic = settings.MAX_SPORADICS_BACKUPS

    number_backups = number_of_backups(project_backup_dir)

    if not (number_backups is None) and (number_backups >= max_sporadic):
        logging.warning("Number of backups (%s) exceeded, the current limit is: %s." % \
                        (number_backups,max_sporadic) )
        return HttpResponse('403 Copy limit exceeded', status=403)

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

    args.append('-n')
    args.append(backup_name)

    args_debug = list(args)
    args_debug.append('-P')
    args_debug.append('**********')
    
    args.append('-P')
    args.append(database.contrasenia)

    logging.warning("Running with params: \n %s \n" % (args_debug))
    try:
        p = subprocess.Popen(args)

        logging.warning("Requested dump: {}".format(backup_name))
        message_user = "200 {}".format(backup_name)

    except Exception as e:
        logging.error('ERROR Exception: %s' % e)
        message_user = "500 Internal Server Error"

    return HttpResponse(message_user, content_type="text/plain")


@validate_basic_http_autorization
@validate_https_request
def api_backup_exists(request):
    user = basic_http_authentication(request)
    if user is None:
        logging.error("Invalid username or password")
        return HttpResponse('401 Unauthorized', status=401)

    logging.info("Validated user: {}".format(user.username))

    if 'filename' in request.GET:
        filename = request.GET['filename']

        file_exist = os.path.isfile(filename)
        if file_exist:
            logging.info("Existing backup filename: {}".format(filename))
            return HttpResponse("true", content_type="text/plain")
        else:
            logging.warning("Backup file does not exist: {}".format(filename))
            return HttpResponse("false", content_type="text/plain")

        
@validate_basic_http_autorization
@validate_https_request
def api_download(request):
    if 'filename' in request.GET and request.GET['filename']:
        filename = request.GET['filename']
    else:
        return HttpResponse('400 Invalid request', status=400)

    user = basic_http_authentication(request)
    if user is None:
        logging.error("Invalid username or password")
        return HttpResponse('401 Unauthorized', status=401)

    logging.info("Validated user for download: {}".format(user.username))

    if not have_file_permissions(user.username,filename):
        logging.error("User without permissions to download")
        return HttpResponse('401 Unauthorized', status=401)

    try:
        file_descriptor = describe_file(filename)
        base =  Base.objects.filter(nombre=file_descriptor['database']) \
                            .filter(servidor__ip=file_descriptor['server'])

        if not base:
            logging.error("No database found")
            return HttpResponse('404 No database found', status=404)

        if len(base) == 1:
            base = base.first()
            base.last_date_download = datetime.datetime.now()
            base.save(update_fields=['last_date_download'])
        else:
            logging.error("The database was not found, or more than one")
            return HttpResponse('404 Invalid amount of database', status=404)

    except Exception as e:
        logging.error ("ERROR Exception: Marking download date. %s" % (e))
        pass
                
    logging.info("Downloading file: %s" % filename)
    attachment_name = os.path.basename(filename)
    response = FileResponse(FileWrapper(file(filename, 'rb')),
                            content_type='application/application/gzip')
    response['Content-Disposition'] = 'attachment; filename="%s"' % attachment_name
    return response
        

@validate_basic_http_autorization
@validate_https_request
def api_last_dump(request):
    user = basic_http_authentication(request)
    if user is None:
        logging.error("Invalid username or password")
        return HttpResponse('401 Unauthorized', status=401)

    logging.info("Validated user to api_backup_exists: {}".format(user.username))

    database=None
    try:
        if 'database_id' in request.GET:
            database_id = int(request.GET['database_id'])
            database = Base.objects.get(pk=database_id)
    except Exception as e:
        logging.error ("ERROR Exception: Incorrect database_id. %s" % (e))

    if not database:
        logging.error("Invalid Database Id")
        return HttpResponse('404 Request not found', status=404)
    
    backup_directory = database.grupo.directorio

    project_backup_dir = os.path.join(settings.DUMPS_DIRECTORY,
                                      backup_directory,
                                      '*/%s*_base-%s_*' % (database.servidor.ip,
                                                            database.nombre) )
    try:
        logging.error("Path to count dumps: %s" % project_backup_dir)

        dumps_list = glob.glob("%s" % project_backup_dir)
        dumps_list.sort(key=lambda x: re.sub(r"^.*_base-","",x))
        last_dump=""
        if len(dumps_list) > 0:
            last_dump = dumps_list[-1]

        logging.warning("Dump list:{}".format(dumps_list))
        logging.warning("Last dump:{}".format(last_dump))
        return HttpResponse(last_dump, content_type="text/plain")
    except Exception as e:
        logging.error("ERROR Exception: {}".format(e))
        return HttpResponse('500 Internal Server Error', status=500)
        pass
