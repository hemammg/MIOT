import os

class Config:
    # General Config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URI = 'sqlite:///app.db'  # Use SQLite for development

class TestingConfig(Config):
    TESTING = True
    DATABASE_URI = 'sqlite:///test.db'  # Use SQLite for testing
