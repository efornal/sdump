
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
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
from .models import Grupo, Servidor, Base, Share, Version, RatticAPI
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
from app.forms import ServidorForm, BaseForm
import json
from .decorators import validate_basic_http_autorization, validate_https_request
import hashlib


def health(request):
    from django.http import HttpResponse
    return HttpResponse(status=200)


def to_encode(text):
    if isinstance(text, bytes):
        return text.decode("utf-8")
    return test


def set_language(request, lang='es'):
    if 'lang' in request.GET:
        lang = request.GET['lang']
    translation.activate(lang)
    request.session[translation.LANGUAGE_SESSION_KEY] = lang
    logging.info("Language changed by the user to '{}'".format(lang))
    return redirect('index')


def show_dump_errors_to_user():
    if hasattr(settings, 'SHOW_DUMP_ERRORS_TO_USER'):
        return settings.SHOW_DUMP_ERRORS_TO_USER
    else:
        return False

    
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


def number_of_backups(path, server=None, database=None):
    '''
    find number of backups for given path, server, and database.
    path must be a glob expression, server and database are optional
    filters to further refine the search
    '''
    logging.error("dir count backup: %s, %s, %s" % (path, server, database))
    try:
        if server and database:
            coll = [ describe_file(p) for p in glob.glob("%s" % path) ]
            filtered = [ f for f in coll if f['database'] == database and f['server'] == server ]
            return len(filtered)
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


def describe_file(file_path):

    descrived_file = {}
    try:
        file_size = filesizeformat(os.path.getsize(file_path))
        file_name = os.path.basename(file_path)
        link_to_share_file = ''
        
        [server,text] = re.split("_base-|_base_con_historico-|_base_sin_hist-",file_name)
        [database,date,time,text] = re.split("_([0-9]{2,4}-[0-9]{2}-[0-9]{2,4})[_|-]([0-9]{2}[-|_][0-9]{2})",text)
        time = time.replace('_',':').replace('-',':')
        fdate = to_date_according_to_text(date)
        date = fdate.strftime("%d-%m-%Y")

        share_file_related = Share.objects.filter(database__nombre=database) \
                                          .filter(name=file_path) \
                                          .first()
        if not share_file_related is None:
            link_to_share_file = reverse('share_dump' ,
                                         kwargs={'filename':share_file_related.hash})
            
        descrived_file = {'file_path': file_path,
                          'file_name': file_name,
                          'link_to_share_file': link_to_share_file,
                          'database': database,
                          'server': server,
                          'size': file_size,
                          'date': date,
                          'time': time, }
    except Exception as e:
        logging.error('ERROR Exception: with file %s, %s' % (file_path,e))
        
    return descrived_file


def describe_files(files):
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

def get_rattic_creds( rattic_id ):
    result = ['','']
    try:
        if not hasattr(settings, 'RATTIC_SERVICE_URL') \
          or not hasattr(settings, 'RATTIC_SERVICE_CREDS'):
            logging.warning("Whithout configurations for rattic")
            return result
        
        api = RatticAPI(
            server = settings.RATTIC_SERVICE_URL,
            creds  = settings.RATTIC_SERVICE_CREDS,
        )
        result = api.get_creds(rattic_id)
    except Exception as e:
        logging.error('ERROR Exception: %s' % e)
    return result

    
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
            db_user, db_pass = get_rattic_creds(request.POST['db_pass_id'])
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
    context.update({'dump_timeout': settings.DUMP_TIMEOUT })
    
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


def get_postgresql_args(request,database):
    args = []
    extra_options = ''
    dump_date = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
    backup_directory = os.path.join( database.grupo.directorio,
                                     settings.SUFFIX_SPORADIC_DUMPS)
    backup_name = os.path.join(settings.DUMPS_DIRECTORY,
                               backup_directory,
                               '%s_base-%s_%s.sql.gz' % (database.servidor.ip,
                                                         database.nombre,
                                                         dump_date) )
    args.append('/usr/bin/pg_dump')

    if 'opt_inserts' in request.POST and request.POST['opt_inserts']=='true':
        args.append('-i')
        
    if 'opt_clean' in request.POST and request.POST['opt_clean']=='true':
        extra_options += ' --clean '
        
    if 'extra_options' in request.POST:
        extra_options += clean_extra_options(request.POST['extra_options'])

    if extra_options:
        args.append('-o')
        args.append(extra_options)

    args.append('-h')
    args.append(database.servidor.ip)

    args.append('-f')
    args.append(backup_name)

    args.append('-d')
    args.append(database.nombre)
    return args



def get_db_credentials(database):
    db_pass = None
    db_user = None
    if database.usuario and database.contrasenia:
        db_pass = database.contrasenia
        db_user = database.usuario
    else:
        if database.password_id:
            logging.warning("Password not defined, using password_id ...")
            db_pass,db_user = get_rattic_creds(database.password_id)
        else:
            logging.error("ERROR: No password or id password to use")
            message_user += "%s\n" % (_('backup_with_mistakes'))
    return db_user, db_pass

@login_required
def make_backup(request):
    database_id = int(request.POST['database_id'])
    database = Base.objects.get(pk=database_id)

    message_user = ''
    args = []
    backup_directory = os.path.join( database.grupo.directorio,
                                     settings.SUFFIX_SPORADIC_DUMPS)
    returned_code = None
    proc_env={}

    # check for maximum sporadick backups
    max_sporadic = 5
    project_backup_dir = os.path.join(settings.DUMPS_DIRECTORY,
                                      backup_directory)
    if hasattr(settings, 'MAX_SPORADICS_BACKUPS'):
        max_sporadic = settings.MAX_SPORADICS_BACKUPS

    number_backups = number_of_backups(
        "{}/*".format(project_backup_dir),
        database.servidor.ip,
        database.nombre
    )

    if not (number_backups is None) and (int(number_backups) >= int(max_sporadic)):
        logging.warning("Number of backups (%s) exceeded, the current limit is: %s." % \
                        (number_backups,max_sporadic) )
        message_user += _('number_backups_exceeded') % {'max_copies':max_sporadic}
        return HttpResponse(message_user, content_type="text/plain")

    if database.servidor.motor == 'postgresql':
        args = get_postgresql_args(request,database)
    
    db_user, db_pass = get_db_credentials(database)
    args.append('-U')
    args.append(db_user)
    logging.warning("Running with params: \n {} \n".format(args))

    
    logging.warning("Making backup ,...")
    try:
        proc_env = os.environ
        proc_env['PGPASSWORD'] = db_pass
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=proc_env)
        out, err = p.communicate()
        returned_code = p.returncode

        if 'opt_share' in request.POST and request.POST['opt_share']=='true':
            if database.alow_sharing:
                share = Share(name=backup_name,
                              hash= hashlib.md5(backup_name.encode()).hexdigest(),
                              database=database)
                logging.warning("Sharing dump file: {}".format(backup_name) )
                share.save()
            else:
                logging.warning("Request to share link dump, but the database {} "\
                                "does not have permissions to share.".format(database))
                message_user += "{}\n".format(_('no_permissions_to_share'))


    except Exception as e:
        logging.error('ERROR Exception: {}'.format(e))
        
    if returned_code:
        logging.error("Dump script error:")
        logging.error(err)
        logging.warning("Dump script output:")
        logging.warning(out)
        logging.warning("Dump script exit code: {}".format(returned_code))
        message_user += "{}\n {}\n".format(_('backup_with_mistakes'),to_encode(out))
        if show_dump_errors_to_user():
            message_user += to_encode(err)
    else:
        message_user += _('backup_finished')
    
    return HttpResponse(message_user, content_type="text/plain")


@login_required
def update_extra_options(request):
    extra_options=""
    if ('database_id' in request.GET) and (int(request.GET['database_id']) > 0):
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
        share_file = Share.objects.get(name=filename)
        if share_file:
            share_file.remove()
            
    except OSError as e:
        logging.warning("Error removing file: %s" % filename)
        logging.warning("Error: %s" % e)
        message = _('error_deleting')
        pass
    except Exception as e:
        logging.error ("ERROR Exception: Deleting share. %s" % (e))
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

    db_user = ''
    db_pass = ''
    if database.usuario and database.contrasenia:
        db_user = database.usuario
        db_pass = database.contrasenia
    else:
        if database.password_id:
            logging.warning("Password not defined, using password_id ...")
            db_user, db_pass = get_rattic_creds(database.password_id)
        else:
            logging.error("ERROR: No password or id password to use")
            return HttpResponse('500 Internal Server Error', status=500)
    
    server = database.servidor
    server_ip = server.ip
    extra_options = ""
    args = []
    backup_directory = os.path.join( database.grupo.directorio,
                                     settings.SUFFIX_SPORADIC_DUMPS)

    dump_date=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
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

    args.append('-t')
    args.append(database.servidor.motor)

    args.append('-U')
    args.append(db_user)

    args.append('-D')
    args.append( os.path.join(settings.DUMPS_DIRECTORY, backup_directory) )

    args.append('-n')
    args.append(backup_name)

    args_debug = list(args)
    args_debug.append('-P')
    args_debug.append('**********')
    
    args.append('-P')
    args.append(db_pass)

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


# sub directory within backup_directory, default all subdirectory
def get_last_dump_name(request,sub_directory='*'):
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
        logging.warning("Invalid Database Id")
        return HttpResponse('404 Request not found', status=404)
    
    backup_directory = database.grupo.directorio
    project_backup_dir = os.path.join(settings.DUMPS_DIRECTORY,
                                      backup_directory,
                                      '%s/%s*_base-%s_*' % (sub_directory,
                                                                database.servidor.ip,
                                                                database.nombre) )
    try:
        logging.info("Path to count dumps: %s" % project_backup_dir)

        dumps_list_0 = glob.glob("%s" % project_backup_dir)
        dumps_list_0.sort(key=lambda x: re.sub(r"^.*_base-","",x))

        # filtrar match exacto en el nombre de la base de datos
        dumps_list = [i for i in dumps_list_0 if re.match('^.*/{}_base-{}{}'.format(
            database.servidor.ip,
            database.nombre,
            '_[0-9]{2,4}-[0-9]{2}-[0-9]{2,4}[_|-][0-9]{2}[-|_][0-9]{2}\.'
        ), i)]

        last_dump=""
        if len(dumps_list) > 0:
            last_dump = dumps_list[-1]
            logging.info("Dumps list: {}".format(dumps_list))
            logging.info("Last dump found: {}".format(last_dump))
            return HttpResponse("200 {}".format(last_dump), content_type="text/plain")
        else:
            logging.warning("The database does not have an available dump.")
            return HttpResponse('404 The database does not have an available dump.', status=404)
 
    except Exception as e:
        logging.error("ERROR Exception: {}".format(e))
        return HttpResponse('500 Internal Server Error', status=500)
        pass

    
@validate_basic_http_autorization
@validate_https_request
def api_periodics_last_dump(request):
    return get_last_dump_name( request,
                                   settings.SUFFIX_PERIODICAL_DUMPS )


@validate_basic_http_autorization
@validate_https_request
def api_sporadics_last_dump(request):
    return get_last_dump_name( request,
                                   settings.SUFFIX_SPORADIC_DUMPS )


@validate_basic_http_autorization
@validate_https_request
def api_last_dump(request):
    return get_last_dump_name( request )


   
@validate_basic_http_autorization
@validate_https_request
def api_get_database_id(request):
    user = basic_http_authentication(request)
    if user is None:
        logging.error("Invalid username or password")
        return HttpResponse('401 Unauthorized', status=401)

    logging.info("Validated user: {}".format(user.username))

    server = ''
    database = ''
    group = ''
    if 'server' in request.GET:
        server = request.GET['server']
    if 'database' in request.GET:
        database = request.GET['database']
    if 'group' in request.GET:
        group = request.GET['group']

    if not server or not database: 
        logging.warning("Database and server name are required")
        return HttpResponse('404 Request not found', status=404)

    try:
        if group:
            db_found = Base.objects.values('id', 'nombre') \
                                   .filter(grupo__nombre=group) \
                                   .filter(servidor__nombre=server) \
                                   .filter(nombre=database)
        else:
            db_found = Base.objects.values('id', 'nombre') \
                                   .filter(servidor__nombre=server) \
                                   .filter(nombre=database)

        if len(db_found) == 1:
            db_found = db_found.first()
            logging.info("Database found: {}-{}".format(db_found['id'],db_found['nombre']))
            return HttpResponse("200 {} {}".format(db_found['id'],db_found['nombre']), \
                                content_type="text/plain",status=200)
        elif len(db_found) > 1: 
            logging.warning("More than one result was found for database:{}, server:{}, group:{}" \
                            .format(database, server, group))
            return HttpResponse('404 More than one result was found', status=404)
        else:
            logging.warning("No results found for database:{}, server:{}, group:{}" \
                            .format(database, server, group))
            return HttpResponse('404 Request not found', status=404)
    
    except Exception as e:
        logging.error ("ERROR Exception: {}".format(e))
        return HttpResponse('500 Internal Server Error', status=500)


def share_dump(request, filename=None):
    if filename is None:
        logging.error("Undefined file name")
        return HttpResponse('404 Request not found', status=404)
    
    try:
        share_file = Share.objects.get(hash=filename)
    except Exception as e:
        logging.error ("ERROR Exception: {}".format(e))
        return HttpResponse('404 Request not found', status=404)

    if not share_file.database.alow_sharing:
        logging.error("The dump is not allowed to be shared.")
        return HttpResponse('404 Request not found', status=404)

    attachment_name = re.sub(r'.+_base-','',share_file.name)

    logging.warning("Exporting file {} with hash {}".format(share_file.name,share_file.hash))
    response = FileResponse(FileWrapper(file(share_file.name, 'rb')),
                            content_type='application/gzip')
    response['Content-Disposition'] = 'attachment; filename={}'.format(attachment_name)
    return response



# Creates or updates the server specified in name parameter.
# If the indicated engine version does not exist, create it.
# Parameters: 
#     nombre, ip, puerto, motor (postgresql/mysql), description, version(9.4, 8.4,..)
# responses (code, message):
#     401: '401 Unauthorized'
#     200: '200 server_id'           # created or updated!
#     404: '404 Request not found'   # another thing
@validate_basic_http_autorization
@validate_https_request
def api_servers_update_or_create(request):

    user = basic_http_authentication(request)
    if user is None:
        logging.error("Invalid username or password")
        return HttpResponse('401 Unauthorized', status=401)
    logging.info("Validated user to api_backup_exists: {}".format(user.username))

    try:
        server = None
        server_form = None
        params = request.GET.copy()
        version_id = None
        status = 'Nothing done'
        logging.info("creating server with params: {}".format(params))

        # obtiene id version, o crea nueva si no existe
        if 'version' in params and params['version']:
            try:
                version = Version.objects.get(nombre="{}".format(params['version'].strip()))
                version_id = version.pk

            except Version.DoesNotExist:
                logging.warning("The version {} does not exist, a new one is created"
                                .format(params['version']))
                new_version = Version(nombre=params['version'])
                new_version.save()
                version_id = new_version.pk
            params['version'] = version_id

            
        if 'nombre' in params and params['nombre']:
            try:
                server = Servidor.objects.get(nombre=params['nombre'])
                server_form = ServidorForm(params, instance=server)
                status = 'Updated'
            except Servidor.DoesNotExist:
                server_form = ServidorForm(params)
                status = 'Created'
            
        if server_form.is_valid():
            server = server_form.save()
            logging.warning("Server: {}, Status: {}".format(server,status))
            return HttpResponse('200 {}'.format(server.pk), status=200)
        else:
            logging.error("Incomplete attributes when creating server")
            
    except Exception as e:
        logging.error(e)

    return HttpResponse('404 Request not found', status=404)



# Creates or updates the database specified in name parameter.
# If the server name or group name is not indicated it is not updated,
# if they are indicated and do not exist it gives an error.
# Parameters: 
#    nombre,usuario,contrasenia,password_id (id_rattic), descripcion,
#    servidor(nombre), grupo(nombre), 
# responses (code, message):
#     401: '401 Unauthorized'
#     200: '200 database_id'           # created or updated!
#     404: '404 Request not found'     # another thing
@validate_basic_http_autorization
@validate_https_request
def api_databases_update_or_create(request):

    user = basic_http_authentication(request)
    if user is None:
        logging.error("Invalid username or password")
        return HttpResponse('401 Unauthorized', status=401)
    logging.info("Validated user to api_backup_exists: {}".format(user.username))

    try:
        database = None
        database_form = None
        params = request.GET.copy()
        server = None
        status = 'Nothing done'
        logging.info("creating database with params: {}".format(params))

        # obtiene el servidor si existe
        if 'servidor' in params and params['servidor']:
            try:
                server = Servidor.objects.get(nombre="{}".format(params['servidor'].strip()))
                params['servidor'] = server.pk
            except Servidor.DoesNotExist:
                logging.error("The server {} does not exist,"
                                .format(params['servidor']))
                return HttpResponse('404 Request not found', status=404)

        # obtiene el grupo si existe
        if 'grupo' in params and params['grupo']:
            try:
                group = Grupo.objects.get(nombre="{}".format(params['grupo'].strip()))
                params['grupo'] = group.pk
            except Grupo.DoesNotExist:
                logging.error("The group {} does not exist,"
                                .format(params['grupo']))
                return HttpResponse('404 Request not found', status=404)

        if 'nombre' in params and params['nombre']:
            try:
                database = Base.objects.get(nombre=params['nombre'])
                database_form = BaseForm(params, instance=database)
                if database_form.is_valid():
                    database.save(update_fields=params)
                    status = 'Updated'
                    return HttpResponse('200 {}'.format(database.pk), status=200)
                else:
                    logging.error("Incomplete attributes when creating database")

            except Base.DoesNotExist:
                database_form = BaseForm(params)
                if database_form.is_valid():
                    database = database_form.save()
                    status = 'Created'
                    return HttpResponse('200 {}'.format(database.pk), status=200)                    
                else:
                    logging.error("Incomplete attributes when creating database")
            
        else:
            logging.error("Incomplete attributes when creating database")
            
    except Exception as e:
        logging.error(e)

    return HttpResponse('404 Request not found', status=404)
