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
from requests import get, post
from six.moves.urllib.parse import urljoin  # noqa


class CmdClient(cmd.Cmd):

    """Line oriented logging client."""

    def __init__(self, server='127.0.0.1', port=7373, *args, **kwargs):
        """Initialize with the given server and port."""
        cmd.Cmd.__init__(self, *args, **kwargs)

        self.server = server
        self.port = port
        self.url = 'http://{server}:{port}'.format(
            server=self.server, port=self.port)

        self.intro = """
Pycslog Copyright (C) 2016 Neil Martinsen-Burrell
This program comes with ABSOLUTELY NO WARRANTY; for details type 'show w'.
This is free software, and you are welcome to redistribute it
under certain conditions; type 'show c' for details.
"""

        self.prompt = '> '

    def _get(self, path, *args, **kwargs):
        """Helper for getting self.url + path."""
        return get(urljoin(self.url, path), *args, **kwargs).json()

    def _post(self, path, *args, **kwargs):
        """Helper for posting to self.url + path."""
        return post(urljoin(self.url, path), *args, **kwargs).json()

    def emptyline(self):
        """Don't repeat previous command."""
        pass

    def do_list(self, args):
        """List all contacts."""
        if args != '':
            print('*** error: list takes no arguments', file=self.stdout)
            return
        contacts = self._get('contacts')
        for contact in contacts:
            print(contact['call'], contact['exchange'], file=self.stdout)

    def do_quit(self, args):  # noqa
        """Quit entering contacts."""
        if args != '':
            print('*** error: quit takes no arguments', file=self.stdout)
            return
        return True

    def default(self, line):
        """This is where lines starting with callsigns get sent."""

        if line == 'EOF':
            return True

        # lines should be of the form "callsign exchange"
        call, exchange = line.split(' ', 1)
        self._post('contact', data={'call': call, 'exchange': exchange})
