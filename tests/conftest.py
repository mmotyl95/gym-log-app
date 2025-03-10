import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def test_app():
    """Create a test instance of the Flask app."""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(test_app):
    """Flask test client."""
    return test_app.test_client()

@pytest.fixture
def init_database(test_app):
    """Creating test user."""
    with test_app.app_context():
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()