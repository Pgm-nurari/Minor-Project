import os

class Config:
    """Base configuration with default settings."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key_here')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 
        'mysql+pymysql://finsight_user:finsight10466266@localhost/finsight_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False

class DevelopmentConfig(Config):
    """Configuration for development."""
    DEBUG = True

class TestingConfig(Config):
    """Configuration for testing."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    """Configuration for production."""
    DEBUG = False
    # Set any additional production-specific settings here.

# Dictionary to help select the configuration based on environment
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
