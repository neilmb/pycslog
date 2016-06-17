
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

"""Test the contacts"""

import datetime
import json

from pycslog.server import Contact

class TestContact:

    """Tests for our contact object"""

    def _usual(self):
        now = datetime.datetime.utcnow()
        return Contact(call='n0fn',
                       exchange='599',
                       frequency=14000,
                       time=now)

    def test_create_default_contact(self):
        """Create a default contact object."""
        contact = Contact()
        assert contact.call is None
        assert contact.exchange is None
        assert contact.frequency is None
        assert contact.time is None

    def test_create_usual_contact(self):
        """Create a usual contact object."""
        contact = self._usual()
        assert contact.call == 'n0fn'
        assert contact.exchange == '599'
        assert contact.frequency == 14000

    def test_contact_mhz(self):
        """Contact works with frequency in MHz"""
        contact = Contact(frequency=14.114)
        assert contact.frequency == 14114

    def test_serialize(self):
        """Contact as a serializable object"""
        serialized = self._usual().serialize()
        assert len(json.dumps(serialized)) > 0
