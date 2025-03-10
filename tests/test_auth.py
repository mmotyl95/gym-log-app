def test_register(client):
    """Test user registration."""
    response = client.post("/auth/register", data={
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "password123",
        "confirm_password": "password123"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Login" in response.data

def test_login(client, init_database):
    """Test successful login."""
    response = client.post("/auth/login", data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Dashboard" in response.data or b"Welcome to Gym Log" in response.data