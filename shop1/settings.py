"""
Django settings for shop1 project.

Generated by 'django-admin startproject' using Django 1.11.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3_eh8f)acfl@rs67en-+7)l0snngazw!^9_5@nmec#qvr-ndi1'

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
    'goods',
    'users',
    'manageuser',
    'captcha',
    'shopping',
    'order',
    'dtpage',
    'play',
    'shop',
    'djcelery',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'shop1.MiddleWare.CheckPower'
]

ROOT_URLCONF = 'shop1.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': False,
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

WSGI_APPLICATION = 'shop1.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'NAME':'shop',
        'USER':'root',
        'PASSWORD':'root',
        'HOST':'localhost',
        'PORT':'3306',
    },
    # 'slave1': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    #     'NAME': 'shop',
    #     'USER': 'root',
    #     'PASSWORD': 'root',
    #     'HOST': 'localhost',
    #     'PORT': '3307',
    # }
}

# DATABASE_ROUTERS = ['myrouter.DBRouter']
# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS=[
    os.path.join(BASE_DIR,'static'),

]
MEDIA_URL = "/uploads/"
MEDIA_ROOT=os.path.join(BASE_DIR,'static')

# LOGIN_URL = '/manage_login/'
#邮箱配置
EMALL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_USER_TLS=False
EMAIL_HOST='smtp.163.com'
EMAIL_PORT=25
EMAIL_HOST_USER='13229557439@163.com'
EMAIL_HOST_PASSWORD='a1261722067'
DEFAULT_FROM_EMAIL=EMAIL_HOST_USER
EMAIL_FROM='13229557439@163.com'

BROKER_URL='redis://127.0.0.1:6379/0'
BROKER_TRANSPORT='redis'
CELERYBEAT_SCHEDULER='djcelery.schedulers.DatabaseScheduler '

#session过期时间
SESSION_COOKIE_AGE = 60 * 30 # 30分钟
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True # 关闭浏览器，则COOKIE失效

