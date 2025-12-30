import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration with default settings."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key_here')
    
    # Database credentials from environment variables
    DB_USERNAME = os.environ.get('DB_USERNAME', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '3306')
    DB_NAME = os.environ.get('DB_NAME', 'finsight_db')
    
    # URL-encode the password to handle special characters
    db_password_encoded = quote_plus(DB_PASSWORD)
    
    # Construct database URI
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 
        f'mysql+pymysql://{DB_USERNAME}:{db_password_encoded}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
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
