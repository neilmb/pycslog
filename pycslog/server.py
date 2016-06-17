
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

import datetime
import json

from flask import Flask, request


app = Flask(__name__)


class Contact(object):  # noqa

    """Represent a single contact."""

    def __init__(self, call=None, exchange=None, frequency=None, time=None):
        """Create a contact with the given information."""
        self.call = call
        self.exchange = exchange

        # Frequency should be in kHz, not MHz
        if frequency is not None:
            if frequency < 100:
                self.frequency = int(1000*frequency)
            else:
                self.frequency = int(frequency)
        else:
            self.frequency = None
        self.time = time

    def serialize(self):
        """Return a serializable object for this contact."""
        return {'call': self.call,
                'exchange': self.exchange,
                'frequency': str(self.frequency),
                'time': self.time.isoformat()}


class Log(object):

    """Represent a single log of contacts."""

    def __init__(self):
        """Log using a list for storage."""
        self._contacts = []

    def log_contact(self, call, exchange, frequency):
        """Save a single contact."""
        current_time = datetime.datetime.utcnow()
        self._contacts.append(Contact(call=call,
                                      exchange=exchange,
                                      frequency=frequency,
                                      time=current_time))
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
    frequency = request.form.get('frequency', None)
    contact_id = LOG.log_contact(call, exchange, frequency)
    return json.dumps({'id': contact_id})


@app.route('/contact/<contact_id>')
def get_contact(contact_id):
    """Retrieve a contact by ID."""
    contact = LOG.get_contact(contact_id).serialize()
    contact['id'] = contact_id
    return json.dumps(contact)


@app.route('/contacts')
def get_contacts():
    """List all contacts."""
    return json.dumps([contact.serialize() for contact in LOG.contacts()])
