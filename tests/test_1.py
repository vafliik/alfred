import tempfile

import os
import pytest
from flask import Flask
from alfred_server import app

from database import db


@pytest.fixture
def app(request):
    db_fd, temp_db_location = tempfile.mkstemp()
    config = {
        'DATABASE': temp_db_location,
        'TESTING': True,
        'DB_FD': db_fd
    }

    test_app = app.test_client()
    test_app.config.update(config)

    with test_app.app_context():
        db.init_app(test_app)
        yield test_app


@pytest.fixture
def client(request, app):
    client = app.test_client()

    def teardown():
        os.close(app.config['DB_FD'])
        os.unlink(app.config['DATABASE'])

    request.addfinalizer(teardown)

    return client


def test_empty_db(client):
    """Start with a blank database."""
    rv = client.get('/')
    assert b'No entries here so far' in rv.data