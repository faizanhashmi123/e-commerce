# Python imports
import os
from os.path import join

# project imports
from .common import *

# uncomment the following line to include i18n
# from .i18n import *


# ##### DEBUG CONFIGURATION ###############################
DEBUG = True

# allow all hosts during development
ALLOWED_HOSTS = ['*']

# adjust the minimal login
# LOGIN_URL = 'core_login'
# LOGIN_REDIRECT_URL = '/'
# LOGOUT_REDIRECT_URL = 'core_login'


##### DATABASE CONFIGURATION ############################
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(PROJECT_ROOT, 'run', 'dev.sqlite3'),
    }
}



# ##### APPLICATION CONFIGURATION #########################
INSTALLED_APPS = DEFAULT_APPS

# AWS_ACCESS_KEY_ID = 'XIDXIUCLD462K3LHF3JW'
# AWS_SECRET_ACCESS_KEY = 'nEhoMjGDNqmg7MMswN1TSSt1avm9c2aWfQi9lAAYQsg'
#
# AWS_STORAGE_BUCKET_NAME = 'koachfilm'
# AWS_S3_ENDPOINT_URL = 'https://fra1.digitaloceanspaces.com'
# AWS_S3_OBJECT_PARAMETERS = {
#     'CacheControl': 'max-age=86400',
# }
# AWS_LOCATION = 'static'
# AWS_DEFAULT_ACL = 'public-read'
# AWS_QUERYSTRING_AUTH = False
#
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# DEFAULT_FILE_STORAGE = 'application.storage_backends.MediaStorage'
#
#
# STATIC_URL = '{}/{}/'.format(AWS_S3_ENDPOINT_URL, AWS_LOCATION)
# MEDIA_URL = '{}/{}/'.format(AWS_S3_ENDPOINT_URL, 'media')
# BUCKET_PATH = f'{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}'
BUCKET_PATH = ''
