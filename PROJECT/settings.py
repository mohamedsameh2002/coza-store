
import os
from pathlib import Path
# from django.contrib.auth.models import User

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG","False").lower() == 'true'

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(" ")


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #app
    'accounts',
    'store',
    'cart',
    'orders',
    'blog',
    'discounts',
    'social_django',
    'ckeditor',
    'paypal.standard.ipn',
    'taggit',
    'django_celery_beat',
    'django_celery_results',


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',#الخاص بالترجمة
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'PROJECT.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',#ترجمة
                'django.contrib.messages.context_processors.messages',
                'store.context_processors.LOOP_PRODUCT_CON',
                'cart.context_processors.COUNTER_ITEM_CON',
                'cart.context_processors.CART_CON',

                'social_django.context_processors.backends',  # <-- Here
                'social_django.context_processors.login_redirect', # <-- Here

                'django.template.context_processors.request',# <-- social shear
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    'social_core.backends.facebook.FacebookOAuth2', # facebook <----
    'social_core.backends.google.GoogleOAuth2',  # google <----
    'django.contrib.auth.backends.ModelBackend',
)


LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = '/accounts/singup/'
LOGOUT_REDIRECT_URL = 'login'




SOCIAL_AUTH_FACEBOOK_KEY = '842559127586703'  # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = '759ec878ed073107760c8ca7f8d694e0'  # App Secret


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '72983575735-g0aglqllplac8edr9cartg38jk26hqhj.apps.googleusercontent.com'  # App ID
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'  # App Secret




WSGI_APPLICATION = 'PROJECT.wsgi.application'
AUTH_USER_MODEL='accounts.Accounts'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

import dj_database_url
# if DEBUG:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': BASE_DIR / 'db.sqlite3',
#         }
#     }
# else:
DATABASES = {
    'default':dj_database_url.parse(os.environ.get("DATABASE_URL"))
}



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

# LANGUAGE_CODE = 'en'#.

LANGUAGE_CODE = 'en-us'
USE_L10N = False
DECIMAL_SEPARATOR = '.'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LANGUAGES = [    #.
    ("en",("English")),
    ("ar",("Arabic")),
]
LOCALE_PATHS = [os.path.join(BASE_DIR,'locale')]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT=os.path.join(BASE_DIR,'static')
STATICFILES_DIRS = [
    # os.path.join(BASE_DIR,'PROJECT/static')
]


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"






# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'




EMAIL_BACKEND= 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST= 'smtp.gmail.com'
EMAIL_HOST_USER= 'asd220.mmc@gmail.com'
EMAIL_HOST_PASSWORD= 'qxjzsbcmebfkymeh'
EMAIL_USE_TLS=True
EMAIL_PORT=587

# EMAIL_HOST_USER= 'sistar32.m@gmail.com'
# EMAIL_HOST_PASSWORD= 'bhwhqqenuzlyispb'



PAYPAL_RECEIVER_EMAIL = 'barbar22.m@gmail.com'
PAYPAL_TEST = True

#Django Admin 




JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-success",
    "accent": "accent-teal",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-info",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "slate",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}



#Celery

CELERY_BROKER_URL=os.environ.get("REDIS_URL"),
CELERY_ACCEPT_CONTENT=['application/json']
CELERY_RESULT_SERIALIZER='json'
CELERY_TASK_SERIALIZER='json'
CELERY_TIMEZONE='UTC'
CELERY_RESULT_BACKEND='django-db'

#Cache


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": os.environ.get("REDIS_URL"),
        'OPTION':{
            'CLIENT_CLASS':'django_redis.client.DefaultClinent'
        }
    }
}
