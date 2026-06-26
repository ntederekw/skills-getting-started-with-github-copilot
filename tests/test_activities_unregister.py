from urllib.parse import quote


def test_unregister_removes_existing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    activity_path = quote(activity_name, safe="")
    participant_email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_path}/participants?email={quote(participant_email, safe='@')}"
    )

    # Assert
    assert response.status_code == 200
    assert participant_email in response.json()["message"]

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert participant_email not in participants


def test_unregister_returns_404_for_unknown_activity(client):
    # Arrange
    missing_activity = "Robotics Club"
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{quote(missing_activity, safe='')}/participants?email={quote(email, safe='@')}"
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_404_when_participant_not_in_activity(client):
    # Arrange
    activity_name = "Chess Club"
    missing_email = "not-registered@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{quote(activity_name, safe='')}/participants?email={quote(missing_email, safe='@')}"
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"


def test_unregister_returns_422_when_email_query_param_missing(client):
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.delete(f"/activities/{quote(activity_name, safe='')}/participants")

    # Assert
    assert response.status_code == 422
