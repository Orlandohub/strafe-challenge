from flask import request, Blueprint
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required
from pony.orm import db_session, commit

from .models import Match, Player

matches_blueprint = Blueprint('matches', __name__)
api = Api(matches_blueprint)

def add_players(players, match):
  # Add players list
  if players:
    for player in players:
      p = Player.get(username=player)
      # If player already exists add object
      # else create object on the fly
      if p:
        match.players.add(p)
      else:
        match.players.create(username=player)


class MatchApi(Resource):
  @db_session
  def get(self, id):
    '''Get match from ID'''
    match = Match.get(id=id)

    if not match:
      return 'No match available with provided ID!', 200

    return {'data': match.to_dict()}, 200

  @jwt_required
  @db_session
  def post(self):
    '''Add a new match.'''
    players = None

    try:
      body = request.get_json()

      if body == None:
        return "No data provided!", 400

      if not body.get("start_date_time"):
        return "You must provide a start date", 400

      # If players provided remove them from body
      # since we cannot add them directly to Player instance
      if body.get('players'):
        # Remove players from body dict
        players = body.pop("players")

      # Create Match instance
      match = Match(**body)

      add_players(players, match)

      commit()
      return {"data": match.to_dict()}, 200
      
    except Exception as e:
      raise e


  @jwt_required
  @db_session
  def put(self, id):
    '''Update Match'''
    players = None
    match = Match.get(id=id)

    if not match:
      return 'No match available with provided ID!', 400

    body = request.get_json()
    if body == None:
      return 200
    
    # If players provided remove them from body
    # since we cannot add them directly to Player instance
    if body.get('players'):
      # Remove players from body dict
      players = body.pop("players")

    match.set(**body)

    add_players(players, match)
    
    commit()
    return {'data': match.to_dict()}, 200


class MatchesApi(Resource):
  @db_session
  def get(self):
    """Get all available matches"""
    matches = Match.select()[:]

    if not matches:
      return 'No matches available!', 200

    result = { "data": [match.to_dict() for match in matches] }
    return result, 200

api.add_resource(MatchApi, '/add-match', '/update-match/<int:id>', '/get-match/<int:id>')
api.add_resource(MatchesApi, '/all-matches')