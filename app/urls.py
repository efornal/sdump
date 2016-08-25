from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static
from app import views

urlpatterns = patterns('app.views',
    url(r'^logout/$', 'logout_view', name='logout'),
    url(r'^login/','login_view', name='login'),
    url(r'^make_backup/','make_backup', name='make_backup'),
    url(r'^download/$', 'download', name='download'),
    url(r'^remove/$', 'remove', name='remove'),
    url(r'^update_servers/','update_servers', name='update_servers'),
    url(r'^update_databases/','update_databases', name='update_databases'),
    url(r'^update_list_backups/','update_list_backups', name='update_list_backups'),
    url(r'^update_extra_options/','update_extra_options', name='update_extra_options'),
    url(r'^$', 'index', name='index'),
)


