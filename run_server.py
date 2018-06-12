#!/usr/bin/env python

# Copyright 2016, 2018 Neil Martinsen-Burrell

# This file is part of Pycslog.

# Pycslog is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pycslog is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pycslog.  If not, see <http://www.gnu.org/licenses/>.

"""Run the server on the default port of 7373."""

from pycslog.server import app

if __name__ == '__main__':
    app.run(port=7373)
