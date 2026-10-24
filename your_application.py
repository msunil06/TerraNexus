"""
Compatibility bridge for Render default deployment start command:
gunicorn your_application.wsgi
"""
from app import create_app

app = create_app()
application = app
