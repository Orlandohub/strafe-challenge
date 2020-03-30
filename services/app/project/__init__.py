import os

from flask import Flask
from flask_jwt_extended import JWTManager


def create_app(test_config=None):
  # Init and config application
  app = Flask(__name__)
  app_settings = os.getenv('APP_SETTINGS')
  app.config.from_object(app_settings)

  # register blueprints
  from project.api.matches import app_blueprint
  app.register_blueprint(app_blueprint)

  # Init JWT
  jwt = JWTManager(app)

  # sanity check
  @app.route('/')
  def ping():
    return { 'status': 'success', 'message': 'pong!' }

  return app