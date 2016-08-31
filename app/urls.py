from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^login/',views.login_view, name='login'),
    url(r'^make_backup/',views.make_backup, name='make_backup'),
    url(r'^download/$', views.download, name='download'),
    url(r'^remove/$', views.remove, name='remove'),
    url(r'^update_servers/',views.update_servers, name='update_servers'),
    url(r'^update_databases/',views.update_databases, name='update_databases'),
    url(r'^update_list_backups/',views.update_list_backups, name='update_list_backups'),
    url(r'^update_extra_options/',views.update_extra_options, name='update_extra_options'),
    url(r'^$', views.index, name='index'),
]


