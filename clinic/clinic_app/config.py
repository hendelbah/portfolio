"""
This module contains all configuration data for web application
"""
import os
import pathlib

from dotenv import load_dotenv

BASE_DIR = pathlib.Path(__file__).parent
load_dotenv(BASE_DIR.parent / '.env')

FLASK_CONFIG = os.getenv('FLASK_CONFIG', default='development')
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', default='super-secret')

MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_SERVER = os.getenv('MYSQL_SERVER', default='localhost')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')


class ProductionConfig:
    """
    Production configurations
    """
    API_KEY = '9T5vOAnb2tDGnRuxh2fhIabi2CIfvtWmi6MrUCNumxHRytuLNZKzd2zxtawQsprV'
    DEBUG = False
    SECRET_KEY = FLASK_SECRET_KEY
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = (f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}'
                               f'@{MYSQL_SERVER}/{MYSQL_DATABASE}?charset=utf8mb4')
    SWAGGER = {
        'uiversion': 3,
        'openapi': '3.0.2'
    }


class TestingConfig(ProductionConfig):
    """
    Configuration for running tests.
    """
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
    DEBUG = True
    SQLALCHEMY_ECHO = False
    WTF_CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class DevelopmentConfig(ProductionConfig):
    """
    Development configurations
    """
    API_KEY = 'qwerty'
    TESTING = True
    SQLALCHEMY_ECHO = True
    DEBUG = True


config_name = {
    'testing': TestingConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig
}

CurrentConfig = config_name[FLASK_CONFIG]
