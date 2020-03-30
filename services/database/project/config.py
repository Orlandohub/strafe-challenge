import os

class BaseConfig:
    """Base configuration"""
    TESTING = False
    SECRET_KEY = 'my_precious'
    JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY')


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DATABASE_URI = os.environ.get('DATABASE_URL')
    PONY = {
      'provider': 'postgres',
      'dsn': DATABASE_URI,
    }


class TestingConfig(BaseConfig):
    """Testing configuration"""
    DATABASE_URI = os.environ.get('DATABASE_TEST_URL')
    TESTING = True


class ProductionConfig(BaseConfig):
    """Production configuration"""
    DATABASE_URI = os.environ.get('DATABASE_URL')
    PONY = {
      'provider': 'postgres',
      'dsn': DATABASE_URI,
    }