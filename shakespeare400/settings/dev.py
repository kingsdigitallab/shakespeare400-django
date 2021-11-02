from .base import *

DEBUG = True
REQUIRE_DEBUG = DEBUG

INTERNAL_IPS = INTERNAL_IPS + ('', )

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'app_shakespeare400_dev',
        'USER': 'app_shakespeare400',
        'PASSWORD': '',
        'HOST': ''
    },
}

LOGGING_LEVEL = logging.DEBUG

LOGGING['loggers']['cms']['level'] = LOGGING_LEVEL
LOGGING['loggers']['shakespeare400']['level'] = LOGGING_LEVEL

TEMPLATES[0]['OPTIONS']['debug'] = True

# -----------------------------------------------------------------------------
# Django Extensions
# http://django-extensions.readthedocs.org/en/latest/
# -----------------------------------------------------------------------------

try:
    import django_extensions  # noqa

    INSTALLED_APPS = INSTALLED_APPS + ('django_extensions',)
except ImportError:
    pass

# -----------------------------------------------------------------------------
# Django Debug Toolbar
# http://django-debug-toolbar.readthedocs.org/en/latest/
# -----------------------------------------------------------------------------

try:
    import debug_toolbar  # noqa

    INSTALLED_APPS = INSTALLED_APPS + ('debug_toolbar',)
    MIDDLEWARE = MIDDLEWARE + (
        'debug_toolbar.middleware.DebugToolbarMiddleware',)
    DEBUG_TOOLBAR_PATCH_SETTINGS = True
except ImportError:
    pass

# -----------------------------------------------------------------------------
# Local settings
# -----------------------------------------------------------------------------

try:
    from .local import *  # noqa
except ImportError:
    print('failed to import local settings')

    from .test import *  # noqa
    print('the project is running with test settings')
    print('please create a local settings file')
