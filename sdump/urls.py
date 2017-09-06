# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import ugettext_lazy as _
from app import views

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('app.urls')),
    url('^api/last_dump',views.api_last_dump, name='api_last_dump'),
]
urlpatterns += i18n_patterns(
    url(r'^', include('app.urls')),
)

