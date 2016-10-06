from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': settings.LOGIN_REDIRECT_URL},
        name='logout'),
    url(r'^make_backup/',views.make_backup, name='make_backup'),
    url(r'^download/$', views.download, name='download'),
    url(r'^remove/$', views.remove, name='remove'),
    url(r'^update_servers/',views.update_servers, name='update_servers'),
    url(r'^update_databases/',views.update_databases, name='update_databases'),
    url(r'^update_list_backups/',views.update_list_backups, name='update_list_backups'),
    url(r'^update_extra_options/',views.update_extra_options, name='update_extra_options'),
    # url(r'^group/(\d+)/?$', views.index, name='index'),
    # url(r'^group/(\d+)/server/(\d+)/?$', views.index, name='index'),
    # url(r'^group/(\d+)/server/(\d+)/database/(\d+)/?$', views.index, name='index'),
    url(r'^group/(?P<group_id>\d+)/$', views.index, name='index'),
    url(r'^group/(?P<group_id>\d+)/server/(?P<server_id>\d+)/$', views.index, name='index'),
    url(r'^group/(?P<group_id>\d+)/server/(?P<server_id>\d+)/database/(?P<database_id>\d+)/$', views.index, name='index'),
    url(r'^$', views.index, name='index'),
]


