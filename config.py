import os
import logging
from urllib.parse import urlparse


logger = logging.getLogger(__name__)


def _default_db_uri():
    """
    Return the default database URI based on environment.
    
    - On Vercel: Use /tmp directory (only writable location)
    - Locally: Use SQLite in current directory
    """
    if os.environ.get('VERCEL') == '1':
        return 'sqlite:////tmp/valtrion.db'
    return 'sqlite:///valtrion.db'


def _database_uri():
    """
    Get the database URI from environment or use default.
    Handles PostgreSQL URL scheme conversion.
    """
    uri = os.environ.get('DATABASE_URL')
    if not uri:
        return _default_db_uri()
    # Convert postgres:// to postgresql:// (required by SQLAlchemy 1.4+)
    if uri.startswith('postgres://'):
        return uri.replace('postgres://', 'postgresql://', 1)
    return uri


def _get_required_env(key, default=None):
    """
    Get environment variable, logging a warning if missing and no default provided.
    """
    value = os.environ.get(key, default)
    if not value and default is None:
        logger.warning(f"Environment variable '{key}' not set. Using empty string.")
        return ''
    return value


class Config:
    """Base Flask configuration."""
    
    # Flask Settings
    FLASK_ENV = os.environ.get('FLASK_ENV', 'production')
    DEBUG = FLASK_ENV == 'development'
    TESTING = False
    
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        logger.warning(
            "SECRET_KEY is not set; using a temporary fallback key so the app can boot."
        )
        SECRET_KEY = 'dev-temporary-key-change-in-production'
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = _database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,  # Verify connections before using them
        'pool_recycle': 3600,    # Recycle connections every hour
    }
    
    # Email Configuration (Gmail)
    # Note: Use Gmail App Password, not regular password
    # Steps: Enable 2FA on Gmail → Account → Security → App Passwords
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = _get_required_env('MAIL_USERNAME', 'valtrionbookings@gmail.com')
    MAIL_PASSWORD = _get_required_env('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = (
        'Valtrion Car Services',
        os.environ.get('MAIL_USERNAME', 'valtrionbookings@gmail.com')
    )
    
    # Payment Gateway (Razorpay)
    RAZORPAY_KEY_ID = _get_required_env('RAZORPAY_KEY_ID')
    RAZORPAY_KEY_SECRET = _get_required_env('RAZORPAY_KEY_SECRET')
    
    # SMS Gateway (Twilio) - Optional
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
    TWILIO_PHONE = os.environ.get('TWILIO_PHONE', '')
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = 3600 * 24  # 24 hours
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # SocketIO Configuration
    SOCKETIO_CORS_ALLOWED_ORIGINS = os.environ.get('SOCKETIO_CORS_ORIGINS', '*').split(',')
    SOCKETIO_ASYNC_MODE = 'threading'
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')


class DevelopmentConfig(Config):
    """Development configuration."""
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = False
    MAIL_DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    MAIL_DEBUG = False
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False


# Select configuration based on environment
def get_config():
    """Return appropriate configuration based on FLASK_ENV."""
    env = os.environ.get('FLASK_ENV', 'production')
    if env == 'development':
        return DevelopmentConfig
    elif env == 'testing':
        return TestingConfig
    else:
        return ProductionConfig