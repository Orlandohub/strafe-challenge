import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,
    Response, current_app
)
from flask_restful import Resource, Api
from flask_jwt_extended import create_access_token
from pony.orm import db_session, commit

from .models import Admin

auth_blueprint = Blueprint('auth', __name__)
api = Api(auth_blueprint)

class SignupApi(Resource):
  @db_session
  def post(self):
    body = request.get_json()
    user = Admin(**body)
    user.hash_password()
    commit()
    id = user.id
    return {'Admin User registered with success!': user.username}, 200


class LoginApi(Resource):
  @db_session
  def post(self):
    body = request.get_json()
    username = body.get('username')
    password = body.get('password')
    
    user = Admin.get(username=username)

    if not user or not user.check_password(password):
      return {"error": "Email or password invalid"}, 401

    # Create our JWTs
    expires = datetime.timedelta(days=7)
    access_token = create_access_token(identity=str(user.id), expires_delta=expires)

    return { 'token': access_token }, 200


api.add_resource(SignupApi, '/auth/signup')
api.add_resource(LoginApi, '/auth/login')
