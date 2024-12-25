from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENGINE: str = 'django.db.backends.mysql'
    DB_NAME: str = 'abobadb'
    DB_USER: str = 'abobauser'
    DB_PASSWORD: str = 'abobas'
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432

    BROKER_URL: str = ''
    ABOBA_TOPIC: str = 'aboba_topic'
    ABOBA_CALLBACK_TOPIC: str = 'callback_aboba_topic'
    GROUP_ID: str = 'airdrop-group'

    DEBUG: bool = False
    SECRET_KEY: str = 'ABOBA'

    MINIO_ACCESS_KEY: str = 'minioadmin'
    MINIO_SECRET_KEY: str = 'minioadmin'
    MINIO_ENDPOINT: str = 'localhost:9000'
    MINIO_SECURE: bool = False
    MINIO_BUCKET_NAME: str = 'memes'


settings = Settings()
