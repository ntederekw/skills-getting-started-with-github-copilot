from urllib.parse import quote


def test_signup_adds_participant_for_existing_activity(client):
    # Arrange
    activity_name = "Chess Club"
    activity_path = quote(activity_name, safe="")
    new_email = "new.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_path}/signup?email={quote(new_email, safe='@')}")

    # Assert
    assert response.status_code == 200
    assert new_email in response.json()["message"]

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert new_email in participants


def test_signup_returns_400_when_student_already_registered(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{quote(activity_name, safe='')}/signup?email={quote(existing_email, safe='@')}"
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_returns_404_for_unknown_activity(client):
    # Arrange
    missing_activity = "Robotics Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{quote(missing_activity, safe='')}/signup?email={quote(email, safe='@')}"
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_returns_422_when_email_query_param_missing(client):
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.post(f"/activities/{quote(activity_name, safe='')}/signup")

    # Assert
    assert response.status_code == 422
