from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Database for development (can use SQLite for easier setup)
# Uncomment below to use SQLite instead of PostgreSQL for development
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# CORS settings for development
CORS_ALLOW_ALL_ORIGINS = True

# Additional development apps
INSTALLED_APPS += [
    'debug_toolbar',
] if 'debug_toolbar' in locals() else []

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
] if 'debug_toolbar' in INSTALLED_APPS else []

# Internal IPs for debug toolbar
INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]

# expense_tracker/settings/development.py