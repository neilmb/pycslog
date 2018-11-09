
"""Test the pycslog webapp."""

from nose.tools import assert_equal

from pycslog.webapp import app

class TestWebapp:

    """Test the web app itself."""

    def setup(self):
        self.app = app.test_client()

    def test_index(self):
        """Get the index page."""
        result = self.app.get('/')
        assert_equal(result.status_code, 200)
