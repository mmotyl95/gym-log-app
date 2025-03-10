def test_register(client):
    """Test user registration."""
    response = client.post("/auth/register", data={
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "password123",
        "confirm_password": "password123"
    }, follow_redirects=True)

    assert b"Account created!" in response.data  # Sprawdzamy, czy dostaliśmy komunikat o sukcesie
    assert response.status_code == 200

def test_login(client, init_database):
    """Test successful login."""
    response = client.post("/auth/login", data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)

    assert b"Logged in successfully!" in response.data  # Czy mamy sukces?
    assert response.status_code == 200