from datetime import datetime
from flask import request, Blueprint
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required
from pony.orm import db_session, commit, select

from .models import db


app_blueprint = Blueprint('app', __name__)
api = Api(app_blueprint)

class Match(Resource):
  @db_session
  def get(self, id):
    """Get match from ID"""
    match = db.Match.get(id=id)

    if not match:
      return 'No match available with provided ID!', 200

    return { "data": match.to_dict() }, 200

class MatchList(Resource):
  @db_session
  def get(self):
    """Get all available matches"""
    matches = db.Match.select()[:]

    if not matches:
      return 'No matches available!', 200

    result = { "data": [match.to_dict() for match in matches] }
    return result, 200

class MatchesApi(Resource):
  @db_session
  def get(self, date):
    """Get all matches on a specific date"""
    try:
      date_time_obj = datetime.strptime(date, '%m-%d-%Y')
    except ValueError:
      return "Please provide date on the following format: mm-dd-yyyy"
    
    matches = select(m for m in db.Match if m.start_date_time.day == date_time_obj.day)

    if not matches:
      return "No matches on given date", 200

    result = {'data': [match.to_dict() for match in matches]}
    return result, 200

# Routes
api.add_resource(Match, '/get-match/<int:id>')
api.add_resource(MatchList, '/all-matches')
api.add_resource(MatchesApi, '/matches/<date>')



