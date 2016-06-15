
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

"""Basic in-memory log server."""

import json

from flask import Flask, request


app = Flask(__name__)


class Log(object):

    """Represent a single log of contacts."""

    def __init__(self):
        """Log using a list for storage."""
        self._contacts = []

    def log_contact(self, call, exchange):
        """Save a single contact."""
        self._contacts.append({'call': call, 'exchange': exchange})
        return len(self._contacts) - 1

    def contacts(self):
        """Get a list of contacts."""
        return self._contacts

    def get_contact(self, contact_id):
        """Return a single contact by id."""
        return self._contacts[int(contact_id)]
LOG = Log()


@app.route('/contact', methods=['POST'])
def log_contact():
    """Log a single contact."""
    call = request.form.get('call', None)
    exchange = request.form.get('exchange', None)
    contact_id = LOG.log_contact(call, exchange)
    return json.dumps({'id': contact_id})


@app.route('/contact/<contact_id>')
def get_contact(contact_id):
    """Retrieve a contact by ID."""
    contact = LOG.get_contact(contact_id)
    contact['id'] = contact_id
    return json.dumps(contact)


@app.route('/contacts')
def get_contacts():
    """List all contacts."""
    return json.dumps(LOG.contacts())
