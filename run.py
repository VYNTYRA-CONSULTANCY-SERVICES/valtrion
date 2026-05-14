"""
Development server entry point for Valtrion.
For production, use wsgi.py or Procfile with gunicorn.
"""
import os
import logging
from app import create_app, socketio, db
from app.sockets import register_sockets

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask app
app = create_app()

# Register SocketIO event handlers
register_sockets(socketio)


def init_db():
    """Initialize database tables."""
    with app.app_context():
        db.create_all()
        logger.info("Database initialized")


if __name__ == '__main__':
    # Initialize database on startup
    init_db()
    
    # Get configuration from environment
    debug = os.environ.get('FLASK_ENV') == 'development'
    port = int(os.environ.get('PORT', 5000))
    
    logger.info(f"Starting server on port {port} (debug={debug})")
    
    # Run the application with SocketIO
    socketio.run(
        app,
        host='0.0.0.0',
        port=port,
        debug=debug,
        use_reloader=debug,
        allow_unsafe_werkzeug=True  # For development only
    )
