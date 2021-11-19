import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URL = 'sqlite:///' + os.path.join(BASEDIR, '../db.sqlite3')


class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URL')


def get_config():
    config_by_name = dict(
        development=DevelopmentConfig,
        production=ProdConfig
    )

    return config_by_name[os.getenv('CONFIG', 'development')]
