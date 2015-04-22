# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView
from api import get_service, get_services, manage_package, get_packages, manage_system_state
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',  # noqa
        TemplateView.as_view(template_name='pages/home.html'),
        name="home"),
    url(r'^about/$',
        TemplateView.as_view(template_name='pages/about.html'),
        name="about"),
    url(r'^admin/$',
        login_required(TemplateView.as_view(template_name='pages/admin.html')),
        name="admin"),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'pages/login.html'}, name="account_login"),

    # Uncomment the next line to enable the admin:
#     url(r'^admin/', include(admin.site.urls)),

    # User management
#     url(r'^users/', include("users.urls", namespace="users")),
#     url(r'^accounts/', include('allauth.urls')),

    # Uncomment the next line to enable avatars
#     url(r'^avatar/', include('avatar.urls')),

    # Your stuff: custom urls go here
    url(r'^api/v1/services/$', csrf_exempt(get_services), name='get_services'),
    url(r'^api/v1/services/(?P<service_name>\w+)/$', csrf_exempt(get_service), name='get_service'),
    url(r'^api/v1/packages/$', csrf_exempt(get_packages), name='get_packages'),
    url(r'^api/v1/packages/(?P<package_name>\w+)/$', csrf_exempt(manage_package), name='manage_package'),
    url(r'^api/v1/system/status/$', csrf_exempt(manage_system_state), name='manage_system_state'),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
