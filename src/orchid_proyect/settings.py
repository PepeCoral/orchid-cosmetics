"""
Django settings for orchid_proyect project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qsl

BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env if present
load_dotenv()

# Print to verify .env is loaded
print("Loading .env file...")
print("ENVIRONMENT from os.getenv:", os.getenv("ENVIRONMENT"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&s=deg$8(kewlz=u8d=))3k34^xwyo%p&od*kxk^jc1#w_2$7f'

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")



# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if ENVIRONMENT != "production" else False

ALLOWED_HOSTS = ["*"]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'orchid_proyect.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'orchid_proyect.wsgi.application'

# Database

if ENVIRONMENT == "production":
    tmpPostgres = urlparse(os.getenv("DATABASE_URL"))
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': tmpPostgres.path.replace('/', ''),
            'USER': tmpPostgres.username,
            'PASSWORD': tmpPostgres.password,
            'HOST': tmpPostgres.hostname,
            'PORT': 5432,
            'OPTIONS': dict(parse_qsl(tmpPostgres.query)),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_USER_MODEL = 'app.User'

# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')

# Cloudinary Configuration - MUST be at module level
if ENVIRONMENT == "production":
    # Add cloudinary apps BEFORE checking config
    INSTALLED_APPS += ["cloudinary_storage", "cloudinary"]

    # Cloudinary configuration
    CLOUDINARY_STORAGE = {
        "CLOUD_NAME": os.getenv("CLOUDINARY_CLOUD_NAME"),
        "API_KEY": os.getenv("CLOUDINARY_API_KEY"),
        "API_SECRET": os.getenv("CLOUDINARY_API_SECRET"),
    }

    # Django 5.2+ uses STORAGES setting (replaces DEFAULT_FILE_STORAGE)
    STORAGES = {
        "default": {
            "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
        },
        "staticfiles": {
            "BACKEND": "cloudinary_storage.storage.StaticHashedCloudinaryStorage",
        },
    }

    MEDIA_URL = '/media/'
    STATIC_URL = '/static/'

else:
    # Local storage
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CSRF_TRUSTED_ORIGINS = [
    "https://orchid-cosmetics.onrender.com",
    "https://myrl-monologic-jules.ngrok-free.dev"
]

# Debug prints
print("=== CLOUDINARY DEBUG INFO ===")
print("ENVIRONMENT:", ENVIRONMENT)
print("DEBUG:", DEBUG)

if ENVIRONMENT == "production":
    print("Cloudinary apps:", "cloudinary" in INSTALLED_APPS, "cloudinary_storage" in INSTALLED_APPS)
    print("STORAGES:", STORAGES if 'STORAGES' in dir() else "NOT SET")
    print("CLOUDINARY_STORAGE:", CLOUDINARY_STORAGE)
    print("Env CLOUD_NAME:", os.getenv("CLOUDINARY_CLOUD_NAME"))
    print("Env API_KEY:", os.getenv("CLOUDINARY_API_KEY"))
    print("Env API_SECRET exists:", bool(os.getenv("CLOUDINARY_API_SECRET")))

print("================================")
