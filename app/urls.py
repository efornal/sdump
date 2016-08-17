from django.conf.urls import patterns, url

from app import views

urlpatterns = patterns('app.views',
    url(r'^logout/$', 'logout_view', name='logout'),
    url(r'^login/','login_view', name='login'),
    url(r'^make_backup/','make_backup', name='make_backup'),
    url(r'^update_servers/','update_servers', name='update_servers'),
    url(r'^update_databases/','update_databases', name='update_databases'),
    url(r'^update_list_backups/','update_list_backups', name='update_list_backups'),
    url(r'^$', 'index', name='index'),
)


