from typing import Any, Dict, List

from pydantic import (
    AnyHttpUrl,
    BaseSettings,
    PostgresDsn,
    RedisDsn,
    validator,
)


class Settings(BaseSettings):

    API: str = '/api'
    DOCS: str = '/docs'
    ADMIN: str = '/admin'
    STARTUP: str = 'startup'
    SHUTDOWN: str = 'shutdown'
    SECRET_KEY: str
    FLASK_ADMIN_SWATCH: str = 'cerulean'

    PROJECT_NAME: str = 'VVPI Backend'
    DESCRIPTION: str = 'VVPI Backend'
    VERSION: str = '0.0.1'

    SWAGGER_UI_PARAMETERS: Dict[str, Any] = {
        'displayRequestDuration': True,
        'filter': True,
    }

    SESSION_TIMEDELTA: Dict[str, int] = {
        'days': 7,
    }

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator('BACKEND_CORS_ORIGINS', pre=True)
    def assemble_cors_origins(
        cls, value: str | List[str],  # noqa: N805, WPS110
    ) -> str | List[str]:
        if isinstance(value, str) and not value.startswith('['):
            return [i.strip() for i in value.split(',')]
        elif isinstance(value, (list, str)):
            return value

        raise ValueError(value)

    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DATABASE_URI: PostgresDsn | None = None

    @validator('DATABASE_URI', pre=True)
    def assemble_db_connection(
        cls, value: str | None, values: Dict[str, Any],  # noqa: N805, WPS110
    ) -> str:
        if isinstance(value, str):
            return value

        return PostgresDsn.build(
            scheme='postgresql+asyncpg',
            user=values.get('DB_USER'),
            password=values.get('DB_PASSWORD'),
            host=values.get('DB_HOST'),
            port=values.get('DB_PORT'),
            path='/{0}'.format(values.get('DB_NAME')),
        )

    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_PASSWORD: str
    REDIS_SESSION: str = 'session:{0}'
    REDIS_URI: RedisDsn | None = None

    @validator('REDIS_URI', pre=True)
    def assemble_redis_connection(
        cls, value: str | None, values: Dict[str, Any],  # noqa: N805, WPS110
    ) -> str:
        if isinstance(value, str):
            return value

        return RedisDsn.build(
            scheme='redis',
            host=values.get('REDIS_HOST'),
            port=values.get('REDIS_PORT'),
            password=values.get('REDIS_PASSWORD'),
        )

    class Config(object):
        case_sensitive = True


settings = Settings()
