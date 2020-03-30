import random

from datetime import datetime, timedelta
from pony.orm import Database, Required, Optional, Set

from flask import current_app
from flask_bcrypt import generate_password_hash, check_password_hash

from .const import MATCH_STATE

db = Database()

class Admin(db.Entity):
  username = Required(str, unique=True)
  password = Required(str)

  def hash_password(self):
    self.password = generate_password_hash(self.password).decode('utf8')
  
  def check_password(self, password):
    return check_password_hash(self.password, password)


class Match(db.Entity):
  players = Set('Player')
  state = Required(str, default=MATCH_STATE[0])
  created_date_time = Required(datetime, sql_default='CURRENT_TIMESTAMP')
  start_date_time = Required(datetime)
  end_date_time = Optional(datetime)
  score = Optional(int, default=0)

  def __init__(self, *args, **kwargs):    
    super().__init__(*args, **kwargs)

    # Match will have a 1 day duration by default
    self.end_date_time = self.start_date_time + timedelta(days=1)

    score = random.randint(0, 10000)
    # Change the game state depending on the current time
    if datetime.now() > self.start_date_time and datetime.now() < self.end_date_time:
      self.state = MATCH_STATE[1]
      self.score = score      
    elif datetime.now() > self.end_date_time:
      self.state = MATCH_STATE[2]
      self.score = score

  def to_dict(self):
    players = self.players
    return {
      "players": [player.to_dict() for player in players],
      "state": self.state,
      "created": self.created_date_time.isoformat(),
      "start_date_time": self.start_date_time.isoformat(),
      "end_date_time": self.end_date_time.isoformat() if self.end_date_time != None else None,
      "score": self.score
    }


class Player(db.Entity):
  match = Set(Match)
  username = Required(str, unique=True)
