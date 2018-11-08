#!/bin/bash
gunicorn --worker-class eventlet -w 1 -b 127.0.0.1:7373 pycslog:app
