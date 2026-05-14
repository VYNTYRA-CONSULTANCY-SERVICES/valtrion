"""
Valtrion Car Services Flask Application Factory
"""
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_socketio import SocketIO
from config import get_config

# Initialize Flask extensions
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()
socketio = SocketIO()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app(config=None):
    """
    Application factory function to create and configure the Flask app.
    
    Args:
        config: Configuration object (uses get_config() if not provided)
    
    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static',
                static_url_path='/static')
    
    # Load configuration
    if config is None:
        config = get_config()
    app.config.from_object(config)
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    
    # Configure SocketIO
    socketio.init_app(
        app,
        cors_allowed_origins=app.config.get('SOCKETIO_CORS_ALLOWED_ORIGINS', '*'),
        async_mode=app.config.get('SOCKETIO_ASYNC_MODE', 'threading'),
        ping_timeout=60,
        ping_interval=25
    )
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Create database tables
    with app.app_context():
        db.create_all()
        logger.info("Database tables created/verified")
    
    # Register blueprints
    _register_blueprints(app)
    
    # Register error handlers
    _register_error_handlers(app)
    
    logger.info("Flask application initialized successfully")
    
    return app


def _register_blueprints(app):
    """Register all blueprint modules with the application."""
    try:
        from app.routes.main import main
        from app.routes.auth import auth
        from app.routes.booking import booking
        from app.routes.admin import admin
        from app.routes.profile import profile
        
        app.register_blueprint(main)
        app.register_blueprint(auth)
        app.register_blueprint(booking)
        app.register_blueprint(admin, url_prefix='/admin')
        app.register_blueprint(profile)
        
        logger.info("All blueprints registered successfully")
    except ImportError as e:
        logger.error(f"Failed to register blueprints: {e}")
        raise


def _register_error_handlers(app):
    """Register error handlers for common HTTP errors."""
    
    @app.errorhandler(404)
    def page_not_found(e):
        """Handle 404 errors."""
        logger.warning(f"404 error: {e}")
        return {
            'error': 'Page not found',
            'status': 404
        }, 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        """Handle 500 errors."""
        logger.error(f"500 error: {e}")
        db.session.rollback()
        return {
            'error': 'Internal server error',
            'status': 500
        }, 500
    
    @app.errorhandler(403)
    def forbidden(e):
        """Handle 403 errors."""
        logger.warning(f"403 error: {e}")
        return {
            'error': 'Forbidden',
            'status': 403
        }, 403
    
    @app.shell_context_processor
    def make_shell_context():
        """Provide database models in Flask shell."""
        from app.models import User, Service, Booking, Mechanic, Review, ChatMessage
        return {
            'db': db,
            'User': User,
            'Service': Service,
            'Booking': Booking,
            'Mechanic': Mechanic,
            'Review': Review,
            'ChatMessage': ChatMessage
        }
