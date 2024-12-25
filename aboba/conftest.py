import django
from aboba.config import settings as config
from django.conf import settings


def pytest_configure():
    settings.configure(
        SECRET_KEY=config.SECRET_KEY,
        INSTALLED_APPS=[
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'rest_framework',
            'aboba.posts',
        ],
        ROOT_URLCONF='aboba.aboba.urls',
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',  # noqa
                'NAME': ':memory:',
            },
        },
        CACHES={
            'default': {
                'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
            },
        },
        REST_FRAMEWORK={
            'DEFAULT_AUTHENTICATION_CLASSES': [
                'rest_framework_simplejwt.authentication.JWTAuthentication',
            ],
            'DEFAULT_PERMISSION_CLASSES': [
                'rest_framework.permissions.AllowAny',
            ],
        },
        LOGGING={
            'version': 1,
            'disable_existing_loggers': False,
            'handlers': {
                'console': {
                    'level': 'DEBUG',
                    'class': 'logging.StreamHandler',
                },
            },
            'loggers': {
                'django': {
                    'handlers': ['console'],
                    'level': 'DEBUG',
                    'propagate': True,
                },
            },
        },
    )

    django.setup()
