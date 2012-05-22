import os
import sys
import logging, logging.handlers

import environment
import logconfig

############################
# Relative Filepaths
############################

path = lambda root,*a: os.path.join(root, *a)
ROOT = os.path.dirname(os.path.abspath(__file__))

############################
# Administrators
############################

ADMINS = ()
MANAGERS = ADMINS

############################
# Deployment Configuration
############################

class DeploymentType:
    PRODUCTION = "PRODUCTION"
    DEV = "DEV"
    SOLO = "SOLO"
    STAGING = "STAGING"
    dict = {
        SOLO: 1,
        PRODUCTION: 2,
        DEV: 3,
        STAGING: 4
    }

if 'DEPLOYMENT_TYPE' in os.environ:
    DEPLOYMENT = os.environ['DEPLOYMENT_TYPE'].upper()
else:
    DEPLOYMENT = DeploymentType.SOLO

def is_solo():
    return DEPLOYMENT == DeploymentType.SOLO

def is_dev():
    return DEPLOYMENT == DeploymentType.DEV

def is_prod():
    return DEPLOYMENT == DeploymentType.PRODUCTION

############################
# Site ID and Debugging 
############################

SITE_ID = DeploymentType.dict[DEPLOYMENT]

DEBUG = DEPLOYMENT != DeploymentType.PRODUCTION
STATIC_MEDIA_SERVER = is_solo() or is_dev()
TEMPLATE_DEBUG = DEBUG
SSL_ENABLED = not DEBUG

INTERNAL_IPS = ('127.0.0.1',)

############################
# Logging 
############################

if DEBUG:
    LOG_LEVEL = logging.DEBUG
else:
    LOG_LEVEL = logging.INFO

############################
# Cache Backend
############################

if is_solo() or is_dev():
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        },
        'notifications': {
            'BACKEND': 'redis_cache.cache.RedisCache',
            'LOCATION': '127.0.0.1:6379',
            'OPTIONS': {
                'DB': 1,
                'PARSER_CLASS': 'redis.connection.HiredisParser'
            }
        }
    }

else:
    CACHES = {
        'default': {
            'BACKEND': 'redis_cache.cache.RedisCache',
            'LOCATION': '209.61.142.151:6379',
            'OPTIONS': {
                'DB': 0,
                'PASSWORD': '&Hunt3RK!ll3r$',
                'PARSER_CLASS': 'redis.connection.HiredisParser'
            }
        },
         'notifications': {
            'BACKEND': 'redis_cache.cache.RedisCache',
            'LOCATION': '209.61.142.151:6379',
            'OPTIONS': {
                'DB': 1,
                'PASSWORD': '&Hunt3RK!ll3r$',
                'PARSER_CLASS': 'redis.connection.HiredisParser'
            }
        }
    }

############################
# E-mail Server 
############################

if is_solo() or is_dev():
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    SENDGRID_EMAIL_HOST = 'smtp.sendgrid.net'
    SENDGRID_EMAIL_PORT = 587
    SENDGRID_EMAIL_USERNAME = 'mavenize'
    SENDGRID_EMAIL_PASSWORD = '$0l$tic3919'

DEFAULT_FROM_EMAIL = "Mavenize Support <admin@mavenize.me>"
CONTACT_EMAIL = 'admin@mavenize.me'

############################
# Internationalization
############################

TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'
USE_I18N = False

############################
# Testing & Coverage
############################

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

COVERAGE_REPORT_HTML_OUTPUT_DIR = 'coverage'
COVERAGE_MODULE_EXCLUDES = ['tests$', 'settings$', 'urls$', 'vendor$',
        '__init__', 'migrations', 'templates', 'django', 'debug_toolbar',
        'core\.fixtures', 'users\.fixtures',]

try:
    import multiprocessing
    cpu_count = multiprocessing.cpu_count()
except ImportError:
    cpu_count = 1

NOSE_ARGS = ['--logging-clear-handlers', '--processes=%s' % cpu_count]

if is_solo():
    try:
        os.mkdir(COVERAGE_REPORT_HTML_OUTPUT_DIR)
    except OSError:
        pass

############################
# Media and Static Files
############################

MEDIA_ROOT = path(ROOT, 'media')
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/static/admin/'
ROOT_URLCONF = 'mavenize.urls'
STATIC_ROOT = path(ROOT, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (path(ROOT, 'assets'),)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

if is_prod():
    CUMULUS = {
        'USERNAME': 'mavenize',
        'API_KEY': '7d93ad331ce171acccca10068da233dc',
        'CONTAINER': 'media',
        'STATIC_CONTAINER': 'static'
    }
    DEFAULT_FILE_STORAGE = 'cumulus.storage.CloudFilesStorage'
    STATICFILES_STORAGE = 'cumulus.storage.CloudFilesStaticStorage'

############################
# Version Information

# Grab the current commit SHA from git - handy for confirming the version deployed on a remote server is the one you think it is.
############################

import subprocess
GIT_COMMIT = subprocess.Popen(['git', 'rev-parse', '--short', 'HEAD'],
    stdout=subprocess.PIPE).communicate()[0].strip()
del subprocess

############################
# Database Configuration
############################

DATABASES = {}

if 'test' in sys.argv:
    DATABASES['default'] = {
        'name': 'testdb',
        'ENGINE': 'django.db.backends.sqlite3'
    }
elif DEPLOYMENT == DeploymentType.PRODUCTION:
    DATABASES['default'] = {
        'NAME': 'mavenize_production',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': '198.101.193.156',
        'PORT': '5432',
        'USER': 'mavenize',
        'PASSWORD': '@u$tr@l1aN912'
    }
elif DEPLOYMENT == DeploymentType.DEV:
    DATABASES['default'] = {
        'NAME': 'mavenize_development',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'localhost',
        'PORT': '5432',
        'USER': 'django',
        'PASSWORD': 'PyDjR0ck$'
    }
elif DEPLOYMENT == DeploymentType.STAGING:
    DATABASES['default'] = {
        'NAME': 'mavenize_staging',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': '198.101.193.156',
        'PORT': '5432',
        'USER': 'mavenize',
        'PASSWORD': '@u$tr@l1aN912'
    }
else:
    DATABASES['default'] = {
        'NAME': 'db',
        'ENGINE': 'django.db.backends.sqlite3',
        'HOST': '',
        'PORT': '',
        'USER': '',
        'PASSWORD': ''
    }

############################
# Message Broker for Celery
############################
import djcelery
djcelery.setup_loader()

BROKER_URL = "redis://mavenize:&Hunt3RK!ll3r$@209.61.142.151:6379:3"
CELERY_RESULT_BACKEND = "redis"
CELERY_REDIS_HOST = "209.61.142.151"
CELERY_REDIS_PORT = "6379"
CELERY_REDIS_DB = 4
CELERY_REDIS_PASSWORD = "&Hunt3RK!ll3r$"

CELERY_ALWAYS_EAGER = is_solo() or is_dev()
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

############################
# South
############################

SOUTH_TESTS_MIGRATE = False
SKIP_SOUTH_TESTS = True

############################
# Logging
############################

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'log_file':{
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': path(ROOT, 'logs/django.log'),
            'maxBytes': '16777216',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'apps': {
            'handlers': ['log_file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
    'root': {
        'handlers': ['console', 'mail_admins'],
        'level': 'INFO'
    },
}

############################
# Debug Toolbar
############################

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'EXTRA_SIGNALS': ['social_auth.signals.pre_update',
                      'social_auth.signals.socialauth_registered']
}

############################
# Application Settings
############################

SECRET_KEY = '8^q6o4zyxy%p!ltd^#t)hqmb_))e5zy^nxg151f7tf)y_@%!9-'

############################
# Sessions
############################

if is_solo() or is_dev():
    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
else:
    SESSION_ENGINE = 'redis_sessions.session'
    SESSION_REDIS_HOST = '209.61.142.151'
    SESSION_REDIS_PORT = 6379
    SESSION_REDIS_DB = 2
    SESSION_REDIS_PASSWORD = '&Hunt3RK!ll3r$'
    SESSION_REDIS_PREFIX = 'session'

############################
# Middleware
############################

middleware_list = [
    'django.middleware.common.CommonMiddleware',
    'announce.middleware.AnnounceCookieMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

if is_solo():
    middleware_list += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]
elif is_dev():
    middleware_list += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        'django.middleware.transaction.TransactionMiddleware',
    ]
else:
    middleware_list += [
        'django.middleware.transaction.TransactionMiddleware',
    ]

MIDDLEWARE_CLASSES = tuple(middleware_list)

############################
# Templates
############################

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

if not is_solo():
    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', TEMPLATE_LOADERS),
    )

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'social_auth.context_processors.social_auth_by_name_backends',
)

TEMPLATE_DIRS = (
    path(ROOT, 'templates')
)

############################
# Applications
############################

apps_list = [
        'django.contrib.auth',
        'django.contrib.admin',
        'django.contrib.contenttypes',
        'django.contrib.sites',
        'django.contrib.sessions',
        'django.contrib.markup',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        'activity_feed',
        'bookmark',
        'item',
        'leaderboard',
        'notification',
        'request',
        'review',
        'social_graph',
        'user_profile',

        'movie',

        'nexus',
        'social_auth',
        'south',
        'sorl.thumbnail',
        'haystack',
        'announce',
        'djcelery',
        'compressor',
]

if is_solo() or is_dev():
    apps_list += [
        'debug_toolbar',
        'django_nose',
        'django_coverage',
    ]

if is_prod():
    apps_list += [
        'cumulus',
        'nexus_redis',
        'sendgrid',
    ]

INSTALLED_APPS = tuple(apps_list)

############################
# Nexus Configuration
############################

NEXUS_REDIS_CONNECTIONS = [
    { 'host': '209.61.142.151',
      'password': '&hunt3rk!ll3r$',
      'db': 0 },
    { 'host': '209.61.142.151',
      'password': '&hunt3rk!ll3r$',
      'db': 1 },
    { 'host': '209.61.142.151',
      'password': '&hunt3rk!ll3r$',
      'db': 2 },
    { 'host': '209.61.142.151',
      'password': '&hunt3rk!ll3r$',
      'db': 3 },
    { 'host': '209.61.142.151',
      'password': '&hunt3rk!ll3r$',
      'db': 4 },
    { 'host': '209.61.142.151',
      'password': '&hunt3rk!ll3r$',
      'db': 5 }
]

############################
# Social Authentication
############################

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.facebook.FacebookBackend',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'
SOCIAL_AUTH_EXTRA_DATA = True
SOCIAL_AUTH_EXPIRATION = 'expires'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/signup'
LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/'

############################
# Facebook 
############################

if is_solo() or is_dev():
    FACEBOOK_APP_ID = '319245824782103'
    FACEBOOK_API_SECRET = 'ce2645caabfeb6e234e00d3769ce1793'
else:
    FACEBOOK_APP_ID = '184293225012617'
    FACEBOOK_API_SECRET = '122e7c7f4489c1e55c6c2589ae8e283d'

FACEBOOK_EXTENDED_PERMISSIONS = ['email', 'create_event', 'publish_stream']

############################
# User Profiles
############################

AUTH_PROFILE_MODULE = 'user_profile.UserProfile'

############################
# Haystack
############################

HAYSTACK_CONNECTIONS = {}

if is_solo() or is_dev():
    HAYSTACK_CONNECTIONS['default'] = {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    }
else:
    HAYSTACK_CONNECTIONS['default'] = {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': '198.101.195.82:8983/solr',
    }

############################
# Announce
############################
if is_prod():
    ANNOUNCE_CLIENT_ADDR = '*:5500'
    ANNOUNCE_API_ADDR = '198.101.193.28:6600'

