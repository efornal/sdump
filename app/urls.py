from django.conf.urls import patterns, url

from app import views

urlpatterns = patterns('app.views',
    url(r'^logout/$', 'logout_view', name='logout'),
    url(r'^login/','login_view', name='login'),
    url(r'^$', 'index', name='index'),
)


