import environ


env = environ.Env()
env.read_env(env.str("../../../../", ".env.staging"))


# DB CONF

ENGINE = env.str('ENGINE', 'django.db.backends.postgresql')
NAME = env.str('DB_NAME', 'abobadb')
USER = env.str('DB_USER', 'abobauser')
PASSWORD = env.str('DB_PASSWORD', 'abobas')
HOST = env.str('DB_HOST', 'localhost')
PORT = env.str('DB_PORT', '5432')


# KAFKA CONF

BROKER_URL = env.str('BROKER_URL', '')
ABOBA_TOPIC = env.str('ABOBA_TOPIC', 'aboba_topic')
ABOBA_CALLBACK_TOPIC = env.str('ABOBA_CALLBACK_TOPIC', 'callback_aboba_topic')

# PROJECT CONF

DEBUG = env.bool('DEBUG', False)
SECRET_KEY = env.str('SECRET_KEY', 'ABOBA')
