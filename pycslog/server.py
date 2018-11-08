
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

import abc
import datetime
import json
import sqlite3

from six import add_metaclass

from flask import Flask, Blueprint, request


app = Flask(__name__)


class Contact:  # noqa

    """Represent a single contact."""

    def __init__(self, call=None, exchange=None, frequency=None, time=None):
        """Create a contact with the given information."""
        self.call = call
        self.exchange = exchange

        # Frequency should be in kHz, not MHz
        if frequency is not None:
            frequency = float(frequency)
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
                'time': self.time.strftime("%Y-%m-%d %H:%M:%S")}

@add_metaclass(abc.ABCMeta)
class LogInterface:

    """Abstract base class for a contact log."""

    @abc.abstractmethod
    def log_contact(self, call, exchange, frequency):
        """Save a single contact."""
        raise NotImplementedError

    @abc.abstractmethod
    def contacts(self):
        """Get a list of all contacts."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_contact(self, contact_id):
        """Get a single contact by ID."""
        raise NotImplementedError

    @abc.abstractmethod
    def clear_log(self):
        """Clear the log."""
        raise NotImplementedError


class MemoryLog(LogInterface):

    """Store a log of contacts in a list in memory."""

    def __init__(self):
        """Log using a list for storage."""
        self.clear_log()

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

    def clear_log(self):
        """Clear the log."""
        self._contacts = []


class SqliteLog(LogInterface):

    """Store a log of contacts in a SQLite database."""

    def __init__(self, filename='pycslog.db'):
        self.conn = sqlite3.connect(filename, check_same_thread=False)
        self.cursor = self.conn.cursor()
        try:
            self._create_table()
        except sqlite3.OperationalError:
            self.conn.rollback()
        finally:
            self.conn.commit()

    @staticmethod
    def _to_contact(row):
        """Convert a row of the database to a dict."""
        return Contact(**{
            'time': datetime.datetime.strptime(row[0], '%Y-%m-%dT%H:%M:%S.%f'),
            'frequency': row[1],
            'call': row[2],
            'exchange': row[3],
        })

    def log_contact(self, call, exchange, frequency):
        """Save a contact row."""
        time = datetime.datetime.utcnow().isoformat()
        result = self.cursor.execute(
            'INSERT INTO log (time, frequency, call, exchange) '
            'VALUES (?, ?, ?, ?)',
            (time, frequency, call, exchange)
        )
        last_id = result.lastrowid
        self.conn.commit()
        return last_id

    def contacts(self):
        """Get a list of contacts."""
        result = self.cursor.execute('SELECT time, frequency, call, exchange FROM log')
        return list(map(self._to_contact, result))

    def get_contact(self, contact_id):
        """Get a single contact by ID."""
        return self._to_contact(
            self.cursor.execute(
                'SELECT time, frequency, call, exchange FROM log '
                'WHERE id=?', (contact_id,)).fetchone())

    def _create_table(self):
        """Make the log table again."""
        self.cursor.execute(
            'CREATE TABLE log '
            '(id integer primary key, '
            'time time, frequency integer, call text, exchange text)'
        )

    def clear_log(self):
        """Clear the log table."""
        self.cursor.execute('DROP TABLE log')
        self._create_table()
        self.conn.commit()


LOG = SqliteLog()


# serve the api from a sub-path /api/...
api = Blueprint('api', __name__)

@api.route('/contact', methods=['POST'])
def log_contact():
    """Log a single contact."""
    call = request.form.get('call', None)
    exchange = request.form.get('exchange', None)
    frequency = request.form.get('frequency', None)
    contact_id = LOG.log_contact(call, exchange, frequency)
    return json.dumps({'id': contact_id})


@api.route('/contact/<contact_id>')
def get_contact(contact_id):
    """Retrieve a contact by ID."""
    contact = LOG.get_contact(contact_id).serialize()
    contact['id'] = contact_id
    return json.dumps(contact)


@api.route('/contacts')
def get_contacts():
    """List all contacts."""
    return json.dumps([contact.serialize() for contact in LOG.contacts()])

app.register_blueprint(api, url_prefix='/api')
