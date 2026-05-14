"""
Flask application entry point.
Exports the Flask app for gunicorn to discover.
"""
from app import create_app

app = create_app()
