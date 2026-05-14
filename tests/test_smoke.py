import os

os.environ.setdefault('SECRET_KEY', 'test-secret-key')
os.environ.setdefault('FLASK_ENV', 'testing')

from app import create_app


def test_create_app_registers_blueprints():
    app = create_app()

    assert app is not None
    assert 'main' in app.blueprints
    assert 'auth' in app.blueprints