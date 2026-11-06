ALLOWED_HOSTS = ['*']
DEBUG = True

DATABASE = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'netbox',
    'USER': 'netbox',
    'PASSWORD': 'netbox',
    'HOST': 'postgres',
    'PORT': '5432',
    'CONN_MAX_AGE': 300,
}

REDIS = {
    'tasks': {
        'HOST': 'redis',
        'PORT': 6379,
        'PASSWORD': '',
        'DATABASE': 0,
        'SSL': False,
    },
    'caching': {
        'HOST': 'redis-cache',
        'PORT': 6379,
        'PASSWORD': '',
        'DATABASE': 1,
        'SSL': False,
    },
}

SECRET_KEY = 'dev-only-insecure-secret-key-do-not-use-in-production'

PLUGINS = ['netbox_custom_field_profiles']

PLUGINS_CONFIG = {
    'netbox_custom_field_profiles': {
        'extra_models': [],
    },
}
