from flask.cli import FlaskGroup

from app import create_app, db
from app.logger import logger

# app = create_app()
cli = FlaskGroup(create_app=create_app)
