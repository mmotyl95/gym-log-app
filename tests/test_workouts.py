def test_add_workout(client, init_database):
    """Test adding a workout."""
    client.post("/auth/login", data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)

    response = client.post("/add_workout", data={
        "exercise": "Bench Press",
        "sets": 3,
        "reps": 10,
        "weight": 80
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Dashboard" in response.data
    assert b"Bench Press" in response.data