"""
Django settings for djangoproject project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
import environ
import psycopg2

from urllib.parse import urlparse
from google.cloud import secretmanager

def get_secret(secret_name):
    client = secretmanager.SecretManagerServiceClient()
    secret_path = client.secret_version_path('phx-01h1yptgmche7jcy01wzzpw2rf', secret_name, 'latest')
    response = client.access_secret_version(request={"name": secret_path})
    return response.payload.data.decode("UTF-8")

# If using environment variables 
env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%au08n9!^x1el5)43!=fpxnav(&nsh9b4m=4c#chx68-1)q+4*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# SECURITY WARNING: It's recommended that you use this when
# running in production. The URL will be known once you first deploy
# to Cloud Run. This code takes the URL and converts it to both these settings formats.
# CLOUDRUN_SERVICE_URL = env("CLOUDRUN_SERVICE_URL", default=None)
# if CLOUDRUN_SERVICE_URL:
#     ALLOWED_HOSTS = [urlparse(CLOUDRUN_SERVICE_URL).netloc]
#     CSRF_TRUSTED_ORIGINS = [CLOUDRUN_SERVICE_URL]
#     SECURE_SSL_REDIRECT = True
#     SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# else:
#     ALLOWED_HOSTS = ["*"]

ALLOWED_HOSTS = [
    '0.0.0.0', 
    '127.0.0.1',
    'hello-world-65z3ddbfoa-nn.a.run.app',
    'hello-world-vlfae7w5dq-nn.a.run.app',
    'hello-world-from-cloud-build-trigger-vlfae7w5dq-nn.a.run.app',
    'hello-world-app-vlfae7w5dq-nn.a.run.app',
    'hello-world-vlfae7w5dq-nn.a.run.app'
    ]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'helloworld',
    "hello_world.apps.HelloworldConfig",
    'whitenoise.runserver_nostatic',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

CSRF_TRUSTED_ORIGINS = [
    'https://hello-world-from-cloud-build-trigger-vlfae7w5dq-nn.a.run.app',
    'https://hello-world-vlfae7w5dq-nn.a.run.app',
]

ROOT_URLCONF = 'djangoproject.urls'

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

WSGI_APPLICATION = 'djangoproject.wsgi.application'

# db_url = get_secret('hello-world-env-secret-DATABASE_URL')
# url = urlparse(db_url)

# # [START cloudrun_django_database_config]
# # Use django-environ to parse the connection string
# DATABASES = {"default": db_url}
# # DATABASES = {"default": env.db()}

# # If the flag as been set, configure to use proxy
# if os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
#     DATABASES["default"]["HOST"] = "127.0.0.1"
#     DATABASES["default"]["PORT"] = 5432

# if 'K_SERVICE' in os.environ: # checks if running in cloud run 
# (VALUES FROM hello-world-env-secret-DATABASE_URL below)
# postgres://hello-world-user:TpMr1FbaoD7ThuX9@//cloudsql/phx-01h1yptgmche7jcy01wzzpw2rf:northamerica-northeast1:hello-world-instance/hello-world-db
# postgresql://hello-world-user:TpMr1FbaoD7ThuX9@localhost/hello-world-db?host=/cloudsql/phx-01h1yptgmche7jcy01wzzpw2rf:northamerica-northeast1:hello-world-instance
# psql "postgresql://hello-world-user:${DB_PASSWORD}@${PRIMARY_INSTANCE_IP}/hello-world-db" (will connect successfully)
# so will  ./cloud-sql-proxy phx-01h1yptgmche7jcy01wzzpw2rf:northamerica-northeast1:hello-world-instance
# echo $PRIMARY_INSTANCE_IP:
# 35.203.114.222 
if os.getenv('K_REVISION'):
    DATABASES = {
        'default': {
            # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'ENGINE': 'django.db.backends.postgresql',
            'HOST': '/cloudsql/phx-01h1yptgmche7jcy01wzzpw2rf:northamerica-northeast1:hello-world-instance',
            # 'HOST': '127.0.0.1',
            'NAME': 'hello-world-db',
            'USER': 'hello-world-user',
            'PASSWORD': 'TpMr1FbaoD7ThuX9',

        }
    }
    #-------------------------
    # DATABASES = {
    #     'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'HOST': '',
    #     'PORT': '',
    #     'NAME': 'hello-world-db',
    #     'USER': 'hello-world-user',
    #     'PASSWORD': 'TpMr1FbaoD7ThuX9',
    #     'OPTIONS': {
    #         'unix_socket': '/cloudsql/phx-01h1yptgmche7jcy01wzzpw2rf:northamerica-northeast1:hello-world-instance',
    #     },
    #     }
    # }

# --------------------
# https://github.com/jazzband/dj-database-url/issues/132
# "postgres://" + user + ":" + password + "@" + urllib.parse.quote("/cloudsql/project_id:region:instance_id") + "/" + database
# database_url = "postgres://user:password@%2Fcloudsql%2Fproject_id%3Aregion%3Ainstance_id/database"

# db_url= 'postgresql://hello-world-user:TpMr1FbaoD7ThuX9%2Fcloudsql%2Fphx-01h1yptgmche7jcy01wzzpw2rf%3Anorthamerica-northeast1%3Ahello-world-instance/hello-world-db'
# config = dj_database_url.parse(db_url)
# config['HOST'] = urllib.parse.unquote(config['HOST'])



#     # Update the 'default' database configuration
# DATABASES['default'] = {
#     'ENGINE': 'django.db.backends.postgresql',
#     'HOST': '/cloudsql/phx-01h1yptgmche7jcy01wzzpw2rf:northamerica-northeast1:hello-world-instance',
#     'PORT': '',
#     'NAME': 'hello-world-db',
#     'USER': 'hello-world-user',
#     'PASSWORD': 'TpMr1FbaoD7ThuX9',
# }

# else:
#     DATABASES = {
#             'default': {
#                 # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
#                 'ENGINE': 'django.db.backends.postgresql',
#                 # 'HOST': '/cloudsql/phx-01h1yptgmche7jcy01wzzpw2rf:northamerica-northeast1:hello-world-instance',
#                 'HOST': '127.0.0.1',
#                 'NAME': url.path[1:],
#                 'USER': url.username,
#                 'PASSWORD': url.password,
#             }
#         }
# # If the flag as been set, configure to use proxy
# if os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
#     DATABASES["default"]["HOST"] = "127.0.0.1"
#     DATABASES["default"]["PORT"] = 5432


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         # 'NAME': BASE_DIR / 'db.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# ---- IF USING PROXY --- (https://cloud.google.com/python/django/run)
# # Use django-environ to parse the connection string
# DATABASES = {"default": env.db()}

# # If the flag as been set, configure to use proxy
# if os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
#     DATABASES["default"]["HOST"] = "127.0.0.1"
#     DATABASES["default"]["PORT"] = 5432


# # ----- IF USING DAN"S SOCKET METHOD --- (DOESN NOT WORK YET!!) -------------------------

# db_url = get_secret('hello-world-env-secret-DATABASE_URL')
# # (VALUES FROM hello-world-env-secret-DATABASE_URL below)
# # postgresql://hello-world-user:TpMr1FbaoD7ThuX9@localhost/hello-world-db?host=/cloudsql/phx-01h1yptgmche7jcy01wzzpw2rf:northamerica-northeast1:hello-world-instance
# # psql "postgresql://hello-world-user:${DB_PASSWORD}@${PRIMARY_INSTANCE_IP}/hello-world-db" (will connect successfully)
# # so will  ./cloud-sql-proxy phx-01h1yptgmche7jcy01wzzpw2rf:northamerica-northeast1:hello-world-instance
# # echo $PRIMARY_INSTANCE_IP:
# # 35.203.114.222
# url = urlparse(db_url)
# DATABASES = {
#     'default': {
#         # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'ENGINE': 'django.db.backends.postgresql',
#         # 'HOST': '/cloudsql/phx-01h1yptgmche7jcy01wzzpw2rf:northamerica-northeast1:hello-world-instance',
#         'HOST': '127.0.0.1',
#         'NAME': url.path[1:],
#         'USER': url.username,
#         'PASSWORD': url.password,
#     }
# }


# modified via https://www.youtube.com/watch?v=cBrn5IM4mA8&t=436s, but also tried many other options (including the options field for host - basically need to set host to local host and have it realize its a socket)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': url.path[1:],
#         'USER': url.username,
#         'PASSWORD': url.password,
#         # query:{
#         #     "unix_sock": "/cloudsql/phx-01h1yptgmche7jcy01wzzpw2rf:northamerica-northeast1:hello-world-instance/.s.PGSQL.5432"#.format(os.environ.get('CLOUD_SQL_CONNECTION_NAME'))
#         # }
#         'OPTIONS': {
#             'options': '-c host=/cloudsql/phx-01h1yptgmche7jcy01wzzpw2rf:northamerica-northeast1:hello-world-instance'
#         },
#         # 'HOST': '/cloudsql/phx-01h1yptgmche7jcy01wzzpw2rf:northamerica-northeast1:hello-world-instance',
#         # 'HOST': 'localhost',
#         # 'PORT': 5432,
#     }
# }
#-------------------------------------------


if os.getenv('GITHUB_WORKFLOW'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'github-actions',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': 'localhost',
            'PORT': '5432'
        }
    }
# else:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.postgresql',
#             'NAME': os.getenv('DB_NAME'),
#             'USER': os.getenv('DB_USER'),
#             'PASSWORD': os.getenv('DB_PASSWORD'),
#             'HOST': os.getenv('DB_HOST'),
#             'PORT': os.getenv('DB_PORT')
#         }
#     }



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIR = [str(BASE_DIR.joinpath('static'))]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


