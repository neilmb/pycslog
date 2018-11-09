
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

import datetime
import json

from nose.tools import assert_equal

from pycslog.server import LOG, SqliteLog, MemoryLog, Contact
from pycslog.webapp import app


class TestMemoryLog:

    def setup(self):
        """Create an SQLite-backed log."""
        self.log = MemoryLog()
        self.id = self.log.log_contact('n0fn', '599', 14000, 'PH')

    def test_log_contact(self):
        """Record a single contact"""
        assert self.id >= 0
        assert len(self.log.contacts()) == 1

    def test_get_contact(self):
        """Get a contact by id"""
        contact = self.log.get_contact(self.id)
        assert contact.time
        assert_equal(contact.call, 'n0fn')
        assert_equal(contact.frequency, 14000)
        assert_equal(contact.exchange, '599')
        assert_equal(contact.mode, 'PH')

    def test_contacts(self):
        """List all contacts"""
        contacts = self.log.contacts()
        assert_equal(len(contacts), 1)

    def test_search(self):
        """Search for a contact."""
        assert_equal(len(self.log.search('n0')), 1)
        assert_equal(len(self.log.search('n')), 1)
        assert_equal(len(self.log.search('n0fnp')), 0)
        assert_equal(len(self.log.search('')), 0)

    def teardown(self):
        """Clear the database."""
        self.log.clear_log()

class TestSqliteLog:

    def setup(self):
        """Create an SQLite-backed log."""
        self.log = SqliteLog()
        self.id = self.log.log_contact('n0fn', '599', 14000, 'PH')

    def test_log_contact(self):
        """Record a single contact"""
        count = self.log.conn.cursor().execute(
            'SELECT COUNT(*) FROM log').fetchone()[0]
        assert self.id >= 0
        assert count == 1, count

    def test_get_contact(self):
        """Get a contact by id"""
        contact = self.log.get_contact(self.id)
        assert contact.time
        assert_equal(contact.call, 'n0fn')
        assert_equal(contact.frequency, 14000)
        assert_equal(contact.exchange, '599')
        assert_equal(contact.mode, 'PH')

    def test_contacts(self):
        """List all contacts"""
        contacts = self.log.contacts()
        assert_equal(len(contacts), 1)

    def test_search(self):
        """Search for a contact."""
        assert_equal(len(self.log.search('n0')), 1)
        assert_equal(len(self.log.search('n')), 1)
        assert_equal(len(self.log.search('n0fnp')), 0)
        assert_equal(len(self.log.search('')), 0)

    def teardown(self):
        """Clear the database."""
        self.log.clear_log()

class TestServer:

    def setup(self):
        """Set up a test server to make requests against."""
        self.app = app.test_client()
        self.app.post('/api/contact',
                      data={'call': 'k3ng',
                            'exchange': '599'})

    def teardown(self):
        """Clear log object."""
        LOG.clear_log()

    def test_contact(self):
        """Record a contact"""
        result = self.app.post('/api/contact',
                               data={'call': 'n0fn',
                                     'exchange': '599'})
        assert_equal(result.status_code, 200)

    def test_contact_id(self):
        """Retrieve a contact by id"""
        result = self.app.get('/api/contact/1')
        assert_equal(result.status_code, 200)
        returned = json.loads(result.get_data(as_text=True))
        assert_equal(returned['call'], 'k3ng')
        assert_equal(returned['exchange'], '599')
        for field in ['call', 'time', 'exchange', 'frequency', 'mode']:
            assert field in returned

    def test_contacts(self):
        """Retrieve all contacts"""
        result = self.app.get('/api/contacts')
        assert_equal(result.status_code, 200)
        returned = json.loads(result.get_data(as_text=True))
        assert_equal(len(returned), 1)

    def test_search(self):
        """Search for a contact."""
        result = self.app.get('/api/search/k3ng')
        assert_equal(result.status_code, 200)
        returned = json.loads(result.get_data(as_text=True))
        assert_equal(len(returned), 1)


class test_contact:

    def test_serialize(self):
        serialized_dict = Contact(call='n0fn',
                                  mode='PH',
                                  exchange='599',
                                  time=datetime.datetime.utcnow(),
                                  frequency=5000).serialize()
        for field in ['call', 'mode', 'exchange', 'time', 'frequency']:
            assert field in serialized_dict
