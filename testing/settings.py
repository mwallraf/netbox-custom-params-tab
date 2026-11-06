SECRET_KEY = 'netbox-custom-field-profiles-test-only-not-for-production'
ALLOWED_HOSTS = ['*']
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party deps required by NetBox
    'django_tables2',
    'mptt',
    'taggit',
    # NetBox core apps (adjust list to match your installed NetBox version)
    'netbox',
    'extras',
    'dcim',
    'ipam',
    'virtualization',
    'circuits',
    'tenancy',
    'users',
    'utilities',
    # Plugin under test
    'netbox_custom_field_profiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'netbox.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

PLUGINS = ['netbox_custom_field_profiles']
PLUGINS_CONFIG = {
    'netbox_custom_field_profiles': {},
}

STATIC_URL = '/static/'
STATIC_ROOT = '/tmp/netbox_static_test/'
MEDIA_URL = '/media/'
MEDIA_ROOT = '/tmp/netbox_media_test/'
