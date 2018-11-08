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

"""A basic command-line Pycslog client."""

from __future__ import print_function

import cmd

from six.moves import urllib  # noqa

from requests import get, post
from tabulate import tabulate


urljoin = urllib.parse.urljoin


class CmdClient(cmd.Cmd):

    """Line oriented logging client."""

    def __init__(self, server='127.0.0.1', port=7373, **kwargs):
        """Initialize with the given server and port."""
        cmd.Cmd.__init__(self, **kwargs)

        self.server = server
        self.port = port
        self.url = 'http://{server}:{port}/api/'.format(
            server=self.server, port=self.port)

        self.intro = """
Pycslog Copyright (C) 2016 Neil Martinsen-Burrell
This program comes with ABSOLUTELY NO WARRANTY; for details type 'show w'.
This is free software, and you are welcome to redistribute it
under certain conditions; type 'show c' for details.
"""

        self._set_frequency(14000)  # also sets prompt

    def _error(self, text):
        """Print error text."""
        print('*** error:', text, file=self.stdout)

    def _get(self, path, *args, **kwargs):
        """Helper for getting self.url + path."""
        return get(urljoin(self.url, path), *args, **kwargs).json()

    def _post(self, path, *args, **kwargs):
        """Helper for posting to self.url + path."""
        return post(urljoin(self.url, path), *args, **kwargs).json()

    def _set_frequency(self, freq):
        """Set the client's frequency"""
        self.frequency = freq
        self.prompt = '{}> '.format(self.frequency)

    def emptyline(self):
        """Don't repeat previous command."""
        pass

    def do_list(self, args):
        """List all contacts."""
        if args != '':
            self._error('list command takes no arguments.')
            return
        contacts = self._get('contacts')
        columns = ['time', 'frequency', 'call', 'exchange']
        print(
            tabulate(
                [[contact[key] for key in columns] for contact in contacts],
                headers=[column.title() for column in columns],
            ),
            file=self.stdout
        )

    def do_quit(self, args):  # noqa
        """Quit entering contacts."""
        if args != '':
            print('*** error: quit takes no arguments', file=self.stdout)
            return False
        return True

    def default(self, line):
        """This is where lines starting with callsigns get sent."""

        if line == 'EOF':
            # True stops the interpreter
            return True

        try:
            freq = int(line.split()[0])
            self._set_frequency(freq)
            return False
        except ValueError:
            pass

        # lines should be of the form "callsign exchange"
        try:
            call, exchange = line.split(' ', 1)
        except ValueError:
            self._error('not a contact, no exchange')
            return False
        self._post('contact', data={'call': call,
                                    'exchange': exchange,
                                    'frequency': self.frequency})
