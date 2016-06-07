
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

from flask import Flask, request
from flask.ext.script import Manager


app = Flask(__name__)
manager = Manager(app)


class Log(object):

    """Represent a single log of contacts."""

    def __init__(self):
        self._contacts = []

    def log_contact(self, call, exchange):
        self._contacts.append({'call': call, 'exchange': exchange})
        return len(self._contacts) - 1

    def contacts(self):
        return self._contacts

    def get_contact(self, contact_id):
        return self._contacts[int(contact_id)]

LOG = Log()

@app.route('/contact', methods=['POST'])
def log_contact():
    call = request.form.get('call', None)
    exchange = request.form.get('exchange', None)
    contact_id = LOG.log_contact(call, exchange)
    return json.dumps({'id': contact_id})

@app.route('/contact/<contact_id>')
def get_contact(contact_id):
    return json.dumps(dict([('id', contact_id)] +
                            LOG.get_contact(contact_id).items()))

@app.route('/contacts')
def get_contacts():
    return json.dumps(LOG.contacts())
