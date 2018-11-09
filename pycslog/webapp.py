
"""The whole pycslog web app."""

from flask import Flask

from .server import api


app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')


@app.route('/')
def index():
    """Get the home page of the web app."""
    return app.send_static_file('index.html')
