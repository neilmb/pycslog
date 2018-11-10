
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
import re

import pytest

from pycslog.server import LOG, SqliteLog, MemoryLog, Contact
from pycslog.webapp import app


# parametrized tests for both log implementations
@pytest.fixture(params=[SqliteLog, MemoryLog])
def sqlite_log_id(request, tmpdir):
    """Create an SQLite-backed log."""
    try:
        log = request.param(str(tmpdir.join('pycslog_test.db')))
    except TypeError:
        log = request.param()
    log_id = log.log_contact('n0fn', '599', 14000, 'PH')
    yield (log, log_id)
    log.clear_log()

def test_log_contact(sqlite_log_id):
    """Record a single contact"""
    log, log_id = sqlite_log_id
    assert log_id >= 0
    assert len(log.contacts()) == 1

def test_log_get_contact(sqlite_log_id):
    """Get a contact by id"""
    log, log_id = sqlite_log_id
    contact = log.get_contact(log_id)
    assert contact.time
    assert contact.call == 'n0fn'
    assert contact.frequency == 14000
    assert contact.exchange == '599'
    assert contact.mode == 'PH'

def test_log_contacts(sqlite_log_id):
    """List all contacts"""
    log, log_id = sqlite_log_id
    contacts = log.contacts()
    assert len(contacts) == 1

def test_log_search(sqlite_log_id):
    """Search for a contact."""
    log, log_id = sqlite_log_id
    assert len(log.search('n0')) == 1
    assert len(log.search('n')) == 1
    assert len(log.search('n0fnp')) == 0
    assert len(log.search('')) == 0


@pytest.fixture
def app_client():
    """Set up a test server to make requests against."""
    _app = app.test_client()
    _app.post('/api/contact',
             data={'call': 'k3ng',
                   'exchange': '599'})
    yield _app
    LOG.clear_log()

def test_app_contact(app_client):
    """Record a contact"""
    result = app_client.post('/api/contact',
                            data={'call': 'n0fn',
                                    'exchange': '599'})
    assert result.status_code == 200

def test_app_contact_id(app_client):
    """Retrieve a contact by id"""
    result = app_client.get('/api/contact/1')
    assert result.status_code == 200
    returned = json.loads(result.get_data(as_text=True))
    assert returned['call'] == 'k3ng'
    assert returned['exchange'] == '599'
    for field in ['call', 'time', 'exchange', 'frequency', 'mode']:
        assert field in returned

def test_app_contacts(app_client):
    """Retrieve all contacts"""
    result = app_client.get('/api/contacts')
    assert result.status_code == 200
    returned = json.loads(result.get_data(as_text=True))
    assert len(returned) == 1

def test_app_search(app_client):
    """Search for a contact."""
    result = app_client.get('/api/search/k3ng')
    assert result.status_code == 200
    returned = json.loads(result.get_data(as_text=True))
    assert len(returned) == 1


def test_serialize_contact():
    serialized_dict = Contact(call='n0fn',
                                mode='PH',
                                exchange='599',
                                time=datetime.datetime.utcnow(),
                                frequency=5000).serialize()
    for field in ['call', 'mode', 'exchange', 'time', 'frequency']:
        assert field in serialized_dict
