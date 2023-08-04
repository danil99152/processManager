import pathlib

from pydantic import conint, constr


class Settings:
    APP_TITLE: constr(min_length=1, max_length=255) = 'Windows Process Manager'
    APP_VERSION: constr(min_length=1, max_length=15) = '1'
    APP_HOST: constr(min_length=1, max_length=15) = str('0.0.0.0')
    APP_PORT: conint(ge=0) = 8000
    APP_PATH: constr(min_length=1, max_length=255) = str(pathlib.Path(__file__).parent.resolve())

    address = 'localhost'
    SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:root@{address}:5432/process'


settings = Settings()
