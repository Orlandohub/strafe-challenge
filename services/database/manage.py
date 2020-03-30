import sys
import unittest

from flask.cli import FlaskGroup
from pony.flask import Pony
from project import create_app

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command()
def test():
    """Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    sys.exit(result)
    

if __name__ == '__main__':
  # Init DB and ORM
  Pony(app)
  from project.api.models import db
  db.bind(**app.config['PONY'])
  db.generate_mapping(create_tables=True)

  def close_db(e=None):
      db = g.pop('db', None)

      if db is not None:
          db.disconnect()

  app.teardown_appcontext(close_db)
  
  cli()
