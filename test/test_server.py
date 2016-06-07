import json

from nose.tools import assert_equal

from pycslog.server import app, LOG

class TestServer(object):

    def setup(self):
        """Set up a test server to make requests against."""
        self.app = app.test_client()
        self.app.post('/contact',
                      data={'call': 'k3ng',
                            'exchange': '599'})

    def teardown(self):
        """Clear log object."""
        LOG._contacts = []

    def test_contact(self):
        """Record a contact"""
        result = self.app.post('/contact',
                               data={'call': 'n0fn',
                                     'exchange': '599'})
        assert_equal(result.status_code, 200)

    def test_contact_id(self):
        """Retrieve a contact by id"""
        result = self.app.get('/contact/0')
        assert_equal(result.status_code, 200)
        returned = json.loads(result.data)
        assert_equal(returned['call'], 'k3ng')
        assert_equal(returned['exchange'], '599')

    def test_contacts(self):
        """Retrieve all contacts"""
        result = self.app.get('/contacts')
        assert_equal(result.status_code, 200)
        returned = json.loads(result.data)
        print result.data
        assert_equal(len(returned), 1)
