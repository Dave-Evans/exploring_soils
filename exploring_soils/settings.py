"""
Django settings for myproject project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import dj_database_url
from decouple import config, Csv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)

DEPLOYED = config("DEPLOYED", default=False, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", cast=Csv())
# For uploaded files
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# print(f"Allowed hosts: {ALLOWED_HOSTS}")
# print(f"Debug state: {DEBUG}")
# print(f"Deployed state: {DEPLOYED}")
# print(f"CSRF origins: {CSRF_TRUSTED_ORIGINS}")
# print(f"Base dir: {BASE_DIR}")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.gis",
    "widget_tweaks",
    "bootstrap4",
    "django_tables2",
    "django_filters",
    "crispy_forms",
    "leaflet",
    "djgeojson",
    "storages",
    ## For authenticating users
    "accounts",
    ## custom app
    "boards",
    ## custom app
    "plotter",
    ## custom app
    "books",
    ## custom app
    "bikemileage",
    ## Kanopy
    "kanopy",
    ## Wisconsin Cover crop citizen science
    "wisccc",
    ## Great Lakes Cover Crop Project
    "glccp",
]

CRISPY_TEMPLATE_PACK = "bootstrap4"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "csp.middleware.CSPMiddleware",
]

CSRF_COOKIE_SAMESITE = "None"
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SECURE = True

CSP_FRAME_ANCESTORS = [
    "https://www.michaelfields.org",
]
CSP_STYLE_SRC = [
    "'self'",
    "'unsafe-inline'",
    "https://maxcdn.bootstrapcdn.com/font-awesome/4.1.0/css/font-awesome.min.css",
    "http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css",
    "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/selectize.js/0.15.2/css/selectize.default.min.css",
    "https://unpkg.com/leaflet@1.3.4/dist/leaflet.css",
    "https://fonts.googleapis.com/css?family=Peralta",
    "https://cdnjs.cloudflare.com/ajax/libs/datepicker/0.6.5/datepicker.min.css",
    "https://cdn.jsdelivr.net/npm/ol@v7.2.2/ol.css",
    "http://cdnjs.cloudflare.com/ajax/libs/leaflet/1.0.3/leaflet.css",
    "https://unpkg.com/leaflet@1.7.1/dist/leaflet.css",
    "https://unpkg.com/leaflet@1.0.1/dist/leaflet.css",
]
CSP_SCRIPT_SRC = [
    "'self'",
    "'unsafe-inline'",
    "https://code.jquery.com/jquery-2.1.0.min.js",
    # "https://code.jquery.com/jquery-3.3.1.slim.min.js",
    
    # "https://code.jquery.com/jquery.js",
    # "http://code.jquery.com/jquery.js",
    "https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.2/jquery.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/d3/4.2.2/d3.min.js",
    "http://d3js.org/d3.v3.min.js",
    "https://d3js.org/d3.v4.js",
    "https://cdn.jsdelivr.net/npm/d3@7",
    "https://cdnjs.cloudflare.com/ajax/libs/d3-legend/2.25.6/d3-legend.min.js",
    "https://d3js.org/d3-scale-chromatic.v1.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/regression/2.0.1/regression.min.js",
    "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/js/bootstrap.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/selectize.js/0.15.2/js/selectize.min.js",
    "https://mathjax.rstudio.com/2.7.9/MathJax.js?config=TeX-AMS-MML_HTMLorMML",
    "http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js",
    "https://challenges.cloudflare.com/turnstile/v0/api.js",
    "https://cdnjs.cloudflare.com/ajax/libs/datepicker/0.6.5/datepicker.min.js",
    "https://cdn.jsdelivr.net/npm/ol@v7.2.2/dist/ol.js",
    "http://cdnjs.cloudflare.com/ajax/libs/leaflet/1.0.3/leaflet.js",
    "https://unpkg.com/leaflet@1.3.4/dist/leaflet.js",    
    "https://unpkg.com/leaflet@1.7.1/dist/leaflet.js",
    "https://unpkg.com/leaflet@1.0.1/dist/leaflet.js",
    
]
CSP_IMG_SRC = [
    "'self'",
    "data:",
    "blob:",
    "http://a.tile.osm.org/",
    "http://b.tile.osm.org/",
    "http://c.tile.osm.org/",
    "http://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/",
    "https://unpkg.com/leaflet@1.3.4/dist/images/",
    "https://unpkg.com/leaflet@1.0.1/dist/images/",
    "https://unpkg.com/leaflet@1.7.1/dist/images/",
    "https://tile.openstreetmap.org",
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.0.3/",
    "http://ows.mundialis.de/services/",
    "https://{}.s3.amazonaws.com/media/private/".format(
        config("AWS_STORAGE_BUCKET_NAME")
    ),
    "https://{}.s3.amazonaws.com/media/private/".format(
        config("AWS_WISC_CC_PHOTO_LOCATION")
    ),
    "https://{}.s3.amazonaws.com/media/private/".format(
        config("AWS_WISC_CC_RESEARCHER_DOC_LOCATION")
    ),
    "https://{}.s3.amazonaws.com/dev/".format(config("AWS_GLCCP_PHOTO_LOCATION")),
    "https://greencover-photos-dev.s3.amazonaws.com/media/private/",
    "https://davemike-wisc-cc-dev.s3.amazonaws.com/media/private/",
]

CSP_FONT_SRC = [
    "'self'",
    "http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/fonts/",
    "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/fonts/",
    "https://fonts.gstatic.com/s/",
    "https://maxcdn.bootstrapcdn.com/font-awesome/4.1.0/fonts/",
]

CSP_FRAME_SRC = [
    "'self'",
    "https://challenges.cloudflare.com/cdn-cgi/challenge-platform/",
]
CSP_CONNECT_SRC = ("'self'","https://data.rcc-acis.org/StnData")

ROOT_URLCONF = "exploring_soils.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "exploring_soils.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# DATABASES = {
# 'default': {
# 'ENGINE': 'django.contrib.gis.db.backends.spatialite',
# 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
# }
# }
DATABASES = {"default": dj_database_url.config(default=config("DATABASE_URL"))}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/Chicago"

USE_I18N = True


USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = "/static/"

if DEBUG and DEPLOYED:
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
elif DEBUG:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, "static")


LOGIN_URL = "login"
LOGOUT_REDIRECT_URL = "wisc_cc_home"
LOGIN_REDIRECT_URL = "wisc_cc_home"


LEAFLET_CONFIG = {
    "SPATIAL_EXTENT": (-96.6, 43.0, -90, 48.5),
    "TILES": "http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    "OVERLAYS": [
        ("Cadastral", "http://server/a/{z}/{x}/{y}.png", {"attribution": "&copy; IGN"})
    ],
    "MINIMAP": True,
    # 'DEFAULT_CENTER': (-94.0, 46.0),
    # 'DEFAULT_ZOOM': 14,
    # 'MIN_ZOOM': 3,
    # 'MAX_ZOOM': 18,
}

## Storage Config

AWS_DEFAULT_ACL = None  # try private?
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")
AWS_WISC_CC_PHOTO_LOCATION = config("AWS_WISC_CC_PHOTO_LOCATION")
AWS_WISC_CC_RESEARCHER_DOC_LOCATION = config("AWS_WISC_CC_RESEARCHER_DOC_LOCATION")
AWS_GLCCP_PHOTO_LOCATION = config("AWS_GLCCP_PHOTO_LOCATION")
AWS_S3_REGION_NAME = config("AWS_S3_REGION_NAME")
AWS_S3_CUSTOM_DOMAIN = "%s.s3.amazonaws.com" % AWS_STORAGE_BUCKET_NAME

AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}

# AWS_STATIC_LOCATION = 'static'
# STATICFILES_STORAGE = 'mysite.storage_backends.StaticStorage'
# STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_STATIC_LOCATION)

AWS_PUBLIC_MEDIA_LOCATION = "media/public"
STORAGES = {
    "default": {
        "BACKEND": "exploring_soils.storage_backends.PublicMediaStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

AWS_PRIVATE_MEDIA_LOCATION = "media/private"
PRIVATE_FILE_STORAGE = "exploring_soils.storage_backends.PrivateMediaStorage"

# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")
#

EMAIL_BACKEND = config(
    "EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_HOST = config("EMAIL_HOST", default="")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
NOTIFY_EMAIL = config("NOTIFY_EMAIL")

DEFAULT_FROM_EMAIL = "Evans Geospatial <noreply@evansgeospatial.com>"
EMAIL_SUBJECT_PREFIX = "[Evans Geospatial] "

CLOUDFLARE_TURNSTILE_SECRET_KEY = config("CLOUDFLARE_TURNSTILE_SECRET_KEY", default="")
