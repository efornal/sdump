from django.conf.urls import patterns, url

from app import views

urlpatterns = patterns('app.views',
    url(r'^$', 'index', name='index'),
)


