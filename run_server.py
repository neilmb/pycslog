#!/usr/bin/env python

"""Run the server on the default port of 7373."""

from pycslog.server import app

if __name__ == '__main__':
    app.run(port=7373)
