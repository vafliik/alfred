import tempfile

import os
import pytest
import alfred_server
import json

from database import db


@pytest.fixture
def app(request):
    config = {
        'SQLALCHEMY_DATABASE_URI': 'sqlite://',
        'TESTING': True,
    }

    test_app = alfred_server.app
    test_app.config.update(config)

    with test_app.app_context():
        db.init_app(test_app)

        db.drop_all()
        db.create_all()

        yield test_app


@pytest.fixture
def client(request, app):
    client = app.test_client()

    return client


def test_empty_db(client):
    """Start with a blank database."""
    rv = client.get('/api/v1/projects')
    assert json.loads(rv.data.decode())["projects"] == []


def test_create_project(client):
    rv = client.post("/api/v1/projects", content_type='application/json', data=json.dumps(dict(
        name="Ruzenka"
    )))
    assert json.loads(rv.data.decode())["id"] == 1
    assert json.loads(rv.data.decode())["name"] == "Ruzenka"
