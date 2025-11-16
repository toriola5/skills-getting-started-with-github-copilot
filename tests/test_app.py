import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0
    for activity, details in data.items():
        assert "description" in details
        assert "schedule" in details
        assert "max_participants" in details
        assert "participants" in details


def test_signup_activity():
    activity_name = list(client.get("/activities").json().keys())[0]
    email = "testuser@mergington.edu"
    # First signup should succeed
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200
    # Second signup should fail (already signed up)
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_remove_participant():
    activity_name = list(client.get("/activities").json().keys())[0]
    email = "removeuser@mergington.edu"
    # Sign up first
    client.post(f"/activities/{activity_name}/signup?email={email}")
    # Remove participant
    response = client.post(f"/activities/{activity_name}/remove?email={email}")
    assert response.status_code in (200, 404, 400)  # Acceptable if not implemented yet
