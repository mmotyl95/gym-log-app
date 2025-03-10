from flask_login import login_user
from app.models import User

def test_add_workout(client, init_database, test_app):
    """Test adding a workout."""
    with test_app.app_context():
        user = User.query.filter_by(email="test@example.com").first()
        login_user(user)  # Symulujemy zalogowanie

    response = client.post("/add_workout", data={
        "exercise": "Bench Press",
        "sets": 3,
        "reps": 10,
        "weight": 80
    }, follow_redirects=True)

    assert b"Workout added successfully!" in response.data
    assert response.status_code == 200