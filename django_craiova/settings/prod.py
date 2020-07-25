from django_craiova.settings.base import *

ALLOWED_HOSTS = ['*']

DEBUG = False

ADMINS = [('Vladu Mihai', 'vladuomihai@gmail.com')]

SERVER_EMAIL = 'vladuomihai@gmail.com'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django_logs.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
