import json
import unittest
import werkzeug
from datetime import datetime

from pony.orm import db_session, select
werkzeug.cached_property = werkzeug.utils.cached_property

from project.tests.base import BaseTestCase

from project.api.models import Match


class TestAppService(BaseTestCase):
    """Tests for the Users Service."""
    @db_session
    def test_app(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])


    @db_session
    def test_single_match(self):
        """Ensure get single match behaves correctly."""
        match = Match.select().first()
        with self.client:
            response = self.client.get(f'/get-match/{match.id}')
            data = json.loads(response.data.decode())
            date = datetime.strptime(data['data']['start_date_time'], "%Y-%m-%dT%H:%M:%S")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(match.start_date_time.day, date.day)


    @db_session
    def test_all_matches(self):
        """Ensure get all matches behaves correctly."""
        match = Match.select()[:]
        with self.client:
            response = self.client.get(f'/all-matches')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']), len(match))


if __name__ == '__main__':
    unittest.main()