import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def test_app():
    """Create a test instance of the Flask app."""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # Testowa baza w pamięci
        "WTF_CSRF_ENABLED": False  # Wyłącz CSRF dla testów
    })

    with app.app_context():
        db.create_all()  # Tworzymy testową bazę danych
        yield app  # Testy działają w tym kontekście
        db.session.remove()
        db.drop_all()  # Usuwamy testową bazę po zakończeniu testów

@pytest.fixture
def client(test_app):
    """Flask test client."""
    return test_app.test_client()

@pytest.fixture
def init_database(test_app):
    """Tworzymy testowego użytkownika."""
    with test_app.app_context():
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()