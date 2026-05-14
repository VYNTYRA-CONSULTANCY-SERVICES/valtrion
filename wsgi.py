"""
WSGI entry point for Vercel deployment.
This file is used by Vercel to run the Flask application.
"""
from app import create_app, socketio, db

# Create the Flask app
app = create_app()


def application(environ, start_response):
    """WSGI application for traditional WSGI servers."""
    return app(environ, start_response)


# For development and testing
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=False, host='0.0.0.0', port=5000)
