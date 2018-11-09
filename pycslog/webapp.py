
"""The whole pycslog web app."""

from flask import Flask, render_template

from .server import api


app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')


@app.route('/')
def index():
    return app.send_static_file('index.html')
