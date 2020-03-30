from flask_testing import TestCase
from project import create_app
from project.api.models import Match
from pony.orm import db_session, commit, delete

app = create_app()

class BaseTestCase(TestCase):
  def create_app(self):
      app.config.from_object('project.config.TestingConfig')

      return app

  @db_session
  def setUp(self):
    Match(start_date_time="07/11/2020")
    Match(start_date_time="07/11/2020")
    Match(start_date_time="07/12/2020")
    commit()

  @db_session
  def tearDown(self):
    Match.select().delete(bulk=True)