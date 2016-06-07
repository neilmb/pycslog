
# Copyright 2016 Neil Martinsen-Burrell

# This file is part of Pycslog.

# Pycslog is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Pycslog is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Pycslog.  If not, see <http://www.gnu.org/licenses/>.

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
        returned = json.loads(result.get_data(as_text=True))
        assert_equal(returned['call'], 'k3ng')
        assert_equal(returned['exchange'], '599')

    def test_contacts(self):
        """Retrieve all contacts"""
        result = self.app.get('/contacts')
        assert_equal(result.status_code, 200)
        returned = json.loads(result.get_data(as_text=True))
        assert_equal(len(returned), 1)
