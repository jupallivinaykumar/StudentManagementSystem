import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-2$+rsx1l-stwq+g!(fngi%52%mvlhpw+$qkl*4i@ij#dlo)#n=' # REPLACE WITH YOUR OWN UNIQUE KEY!

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
    'core',
    'students',
    'staff',
    'courses',
    'attendance',
    'results',
    'feedback_app',
    'leave_app',
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

ROOT_URLCONF = 'student_management_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [], # Keep this empty if you follow app-level templates structure
        'APP_DIRS': True, # This tells Django to look for 'templates' folders inside each app
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

WSGI_APPLICATION = 'student_management_system.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'admin', # REPLACE WITH YOUR ACTUAL POSTGRESQL PASSWORD!
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata' # Changed to India Standard Time

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/' # Consolidated and correct STATIC_URL

# This is where Django will look for additional static files
# that are not tied to a specific app's 'static/' directory.
STATICFILES_DIRS = [ # <--- ADDED THIS SECTION
    BASE_DIR / 'static', # Points to your project-level static folder
]
# This is the directory where 'python manage.py collectstatic' will gather
# all static files (from apps and STATICFILES_DIRS) for deployment.
STATIC_ROOT = BASE_DIR / 'static_cdn'

# Media files (user uploaded content)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'core.CustomUser'


# Authentication URL Settings
# These refer to URL NAMES from your urls.py, not direct paths like '/accounts/login/'
LOGIN_URL = 'login' # <--- CRITICAL CHANGE: Use URL NAME 'login'
LOGIN_REDIRECT_URL = 'admin_dashboard' # Default redirect after successful login
LOGOUT_REDIRECT_URL = 'login' # Redirect after logout (uses URL name 'login')

# Email settings (for signup notifications and password resets)
# For testing: Prints emails to console for debugging
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' 

# For real email: (Uncomment and configure these for production)
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.example.com' 
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your_email@example.com'
# EMAIL_HOST_PASSWORD = 'YOUR_EMAIL_APP_PASSWORD_OR_API_KEY'
# DEFAULT_FROM_EMAIL = 'noreply@yourdomain.com'

ADMINS = [
    ('System Admin', 'your_admin_email@example.com'), # REPLACE with your admin's name and actual email
]
SERVER_EMAIL = ADMINS[0][1]