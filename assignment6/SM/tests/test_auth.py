import pytest
from app import create_app, db as _db
from app.models import User
import os

os.environ["FLASK_ENV"] = "testing"


@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        _db.create_all()
        test_user = User(username="testuser")
        test_user.set_password("testpassword")
        _db.session.add(test_user)
        _db.session.commit()
        yield app
        _db.drop_all()


def test_login_valid(app):
    with app.test_client() as client:
        response = client.post(
            "/auth/login",
            data={"username": "testuser", "password": "testpassword"},
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert b"Welcome" in response.data


def test_login_invalid(app):
    with app.test_client() as client:
        response = client.post(
            "/auth/login", data={"username": "wronguser", "password": "wrongpassword"}
        )
        assert response.status_code == 200
        assert b"Invalid username or password" in response.data


def test_register(app):
    with app.test_client() as client:
        response = client.post(
            "/auth/register",
            data={"username": "newuser", "password": "newpassword"},
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert b"Login" in response.data

        new_user = User.query.filter_by(username="newuser").first()
        assert new_user is not None
        assert new_user.username == "newuser"
