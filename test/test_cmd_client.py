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

from six import StringIO

from nose.tools import assert_equal, assert_regexp_matches
from wsgi_intercept import interceptor

from pycslog import cmd_client
from pycslog.server import app

class TestCmdClient:

    def run_commands(self, commands):
        """Run the given commands and return the output.

        Commands should be specified as a single string with newlines
        separating the commands. Output is returned as a single string
        with newlines separating the responses.
        """
        command_input = StringIO(commands)
        output = StringIO()
        self.client = cmd_client.CmdClient(stdin=command_input, stdout=output)
        self.client.use_rawinput = False
        self.client.cmdloop()

        # trim off the intro and its newline
        return output.getvalue()[len(self.client.intro)+1:]

    def setup(self):
        """Set up a server for testing."""
        self.intercept = interceptor.RequestsInterceptor(lambda: app, host='127.0.0.1', port=7373)
        self.intercept.__enter__()

    def teardown(self):
        self.intercept.__exit__(None, None, None)

    def test_quit(self):
        """Quit command works"""
        output = self.run_commands('quit\n')
        assert output.endswith('> ')

    def test_quit_error(self):
        """Quit command fails with arguments"""
        output = self.run_commands('quit now\n')
        assert '*** error' in output

    def test_list(self):
        output = self.run_commands('n0fn 599\nlist\n')
        assert_regexp_matches(output, '\s+14000\s+n0fn\s+599\n14000> ')

    def test_list_error(self):
        """List command fails with arguments"""
        output = self.run_commands('list more stuff\n')
        assert '*** error' in output

    def test_empty_line(self):
        """Empty line does nothing"""
        output = self.run_commands('\n')
        assert output == '14000> 14000> ', output

    def test_frequency_change(self):
        """Number changes frequency"""
        output = self.run_commands('7000\n')
        assert output.endswith('7000> ')

    def test_list_multiple(self):
        """List multiple contacts on different frequencies."""
        output = self.run_commands("""7000
n0fn 599
14000
n0fn 339
list
""")
        assert "Time" in output
        assert_regexp_matches(output, r'7000\s+n0fn\s+599')

    def test_short_contact_error(self):
        """Short line is an error."""
        output = self.run_commands('show')
        assert '*** error' in output
