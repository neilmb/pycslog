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


"""Run the command line client."""

from argparse import ArgumentParser

from pycslog.cmd_client import CmdClient

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--server', default='127.0.0.1')
    parser.add_argument('--port', default=7373)
    args = parser.parse_args()

    CmdClient(server=args.server, port=args.port).cmdloop()
