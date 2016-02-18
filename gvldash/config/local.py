# -*- coding: utf-8 -*-
'''
Local Configurations

- Runs in Debug mode
- Uses console backend for emails
- Use Django Debug Toolbar
'''
import os

from configurations import values

from .common import Common


class Local(Common):

    # DEBUG
    DEBUG = values.BooleanValue(True)
    TEMPLATE_DEBUG = DEBUG
    # END DEBUG

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    GVLDASH_PACKAGE_REGISTRY_URL = 'file://' + \
        PROJECT_ROOT + "/../package_registry.yml.sample"

    # INSTALLED_APPS
    INSTALLED_APPS = Common.INSTALLED_APPS
    # END INSTALLED_APPS

    # Mail settings
    EMAIL_HOST = "localhost"
    EMAIL_PORT = 1025
    EMAIL_BACKEND = values.Value(
        'django.core.mail.backends.console.EmailBackend')
    # End mail settings

    # django-debug-toolbar
    # MIDDLEWARE_CLASSES = Common.MIDDLEWARE_CLASSES + ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    # INSTALLED_APPS += ('debug_toolbar',)

    INTERNAL_IPS = ('127.0.0.1',)

#    DEBUG_TOOLBAR_CONFIG = {
#        'DISABLE_PANELS': [
#            'debug_toolbar.panels.redirects.RedirectsPanel',
#        ],
#        'SHOW_TEMPLATE_CONTEXT': True,
#    }
    # end django-debug-toolbar

    # Your local stuff: Below this line define 3rd party libary settings
