
import os
from pathlib import Path
# from django.contrib.auth.models import User

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-o4xq8g!ipn=yfp^ebyu9l8*!f2&m*jbv!qqc-#0dz)+tvvm_m2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    #app
    'accounts',
    'store',
    'cart',
    'orders',
    'blog',
    'discounts',
    'communication',
    'social_django',
    'ckeditor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
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

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
    "/var/www/static/",
]

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')






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







#jazzmin=======================================================


# JAZZMIN_SETTINGS = {
#     "site_title": "your_site_name",
#     "site_header": "your_site_header",
#     "site_brand": "your_site_brand",
#     "site_icon": "images/favicon.png",
#     # Add your own branding here
#     "site_logo": None,
#     "welcome_sign": "Welcome to the your_site_name",
#     # Copyright on the footer
#     "copyright": "your_site_name",
#     "user_avatar": None,
#     ############
#     # Top Menu #
#     ############
#     # Links to put along the top menu
#     "topmenu_links": [
#         # Url that gets reversed (Permissions can be added)
#         {"name": "your_site_name", "url": "home", "permissions": ["auth.view_user"]},
#         # model admin to link to (Permissions checked against model)
#         {"model": "auth.User"},
#     ],
#     #############
#     # Side Menu #
#     #############
#     # Whether to display the side menu
#     "show_sidebar": True,
#     # Whether to aut expand the menu
#     "navigation_expanded": True,
#     # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
#     # for the full list of 5.13.0 free icon classes
#     "icons": {
#         "auth": "fas fa-users-cog",
#         "auth.user": "fas fa-user",
#         "users.User": "fas fa-user",
#         "auth.Group": "fas fa-users",
#         "admin.LogEntry": "fas fa-file",
#     },
#     # # Icons that are used when one is not manually specified
#     "default_icon_parents": "fas fa-chevron-circle-right",
#     "default_icon_children": "fas fa-arrow-circle-right",
#     #################
#     # Related Modal #
#     #################
#     # Use modals instead of popups
#     "related_modal_active": False,
#     #############
#     # UI Tweaks #
#     #############
#     # Relative paths to custom CSS/JS scripts (must be present in static files)
#     # Uncomment this line once you create the bootstrap-dark.css file
#     # "custom_css": "css/bootstrap-dark.css",
#     "custom_js": None,
#     # Whether to show the UI customizer on the sidebar
#     "show_ui_builder": True,
#     ###############
#     # Change view #
#     ###############
#     "changeform_format": "horizontal_tabs",
#     # override change forms on a per modeladmin basis
#     "changeform_format_overrides": {
#         "auth.user": "collapsible",
#         "auth.group": "vertical_tabs",
#     },
# }



# JAZZMIN_UI_TWEAKS = {
#     "navbar_small_text": False,
#     "footer_small_text": False,
#     "body_small_text": False,
#     "brand_small_text": False,
#     "brand_colour": "navbar-success",
#     "accent": "accent-teal",
#     "navbar": "navbar-dark",
#     "no_navbar_border": False,
#     "navbar_fixed": False,
#     "layout_boxed": False,
#     "footer_fixed": False,
#     "sidebar_fixed": False,
#     "sidebar": "sidebar-dark-info",
#     "sidebar_nav_small_text": False,
#     "sidebar_disable_expand": False,
#     "sidebar_nav_child_indent": False,
#     "sidebar_nav_compact_style": False,
#     "sidebar_nav_legacy_style": False,
#     "sidebar_nav_flat_style": False,
#     "theme": "cyborg",
#     "dark_mode_theme": None,
    
#     "button_classes": {
#         "primary": "btn-primary",
#         "secondary": "btn-secondary",
#         "info": "btn-info",
#         "warning": "btn-warning",
#         "danger": "btn-danger",
#         "success": "btn-success",
#     },
# }