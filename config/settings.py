import os
from pathlib import Path
from config.custom_config import UNFOLD, setup_logging

# ======================================= BASE SETTINGS =======================================

BASE_DIR = Path(__file__).resolve().parent.parent

SITE_ID = 1

SECRET_KEY = 'django-insecure-%cq-(md-*c872)6y31u!!k_ry6rp!+4a_ptd(l!5$rf)@n!k&+'

DEBUG = True

ALLOWED_HOSTS = ['*']

# ======================================= FEATURE FLAGS =======================================

DB = False  # True bo'lsa PostgreSQL, False bo'lsa SQLite
ENABLE_SILK = "1"
LOGGING_STATUS = True
UNFOLD = UNFOLD

# ======================================= INSTALLED APPS =======================================

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    # Unfold admin theme
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "unfold.contrib.import_export",
    "unfold.contrib.guardian",
    "unfold.contrib.simple_history",
    
    # API & Documentation
    'rest_framework',
    'drf_yasg',
    
    # CORS
    'corsheaders',
    
    # Performance monitoring
    *(["silk"] if ENABLE_SILK else []),
    
    # Text editor (commented out)
    # 'ckeditor',
    # 'ckeditor_uploader',
]

CUSTOM_APPS = [
    'main',
]

INSTALLED_APPS = THIRD_PARTY_APPS + DJANGO_APPS + CUSTOM_APPS

# ======================================= MIDDLEWARE =======================================

CORS_ALLOW_ALL_ORIGINS = True

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    *(["silk.middleware.SilkyMiddleware"] if ENABLE_SILK else []),
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ======================================= SILK CONFIGURATION =======================================

SILKY_AUTHENTICATION = True        # Faqat login bo'lganlar kira oladi
SILKY_AUTHORISATION = True         # Faqat staff/superuser ko'ra oladi
SILKY_PYTHON_PROFILER = False      # Python kodini profiling qilish
SILKY_ANALYZE_QUERIES = True       # N+1 va sekin SQL larni aniqlash
SILKY_INTERCEPT_PERCENT = 100      # 100% so'rovlarni yozib borish
SILKY_MAX_REQUEST_BODY_SIZE = 1024 * 128   # Maksimal request hajmi (128KB)
SILKY_MAX_RESPONSE_BODY_SIZE = 1024 * 256  # Maksimal javob hajmi (256KB)
SILKY_MAX_RECORDED_REQUESTS = 10000        # Saqlanadigan so'rovlar soni
SILKY_META = True

# ======================================= URLS & WSGI =======================================

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

# ======================================= DATABASE =======================================

if DB:
    # PostgreSQL konfiguratsiyasi
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': '',
            'USER': '',
            'PASSWORD': '',
            'HOST': 'localhost' if not DEBUG else 'IP adress serverniki',
            'PORT': '5432',
        }
    }
else:
    # SQLite konfiguratsiyasi
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ======================================= AUTHENTICATION =======================================

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

# ======================================= INTERNATIONALIZATION =======================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ======================================= STATIC & MEDIA FILES =======================================

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ======================================= DEFAULT SETTINGS =======================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ======================================= LOGGING =======================================

if LOGGING_STATUS:
    setup_logging()