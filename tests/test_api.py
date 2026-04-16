"""
API test suite for Mergington High School activities management system.

Uses AAA (Arrange-Act-Assert) pattern with test classes organized by endpoint.
Each test follows the pattern:
- Arrange: Fixture provides client + isolated app state
- Act: Call the endpoint with test data
- Assert: Verify status code, response content, and side effects
"""

import pytest
from fastapi.testclient import TestClient


class TestActivities:
    """Test suite for GET /activities endpoint"""

    def test_get_activities_returns_200(self, client: TestClient):
        """
        Arrange: Client fixture provides fresh app instance
        Act: Call GET /activities
        Assert: Response status is 200
        """
        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200

    def test_get_activities_returns_all_nine_activities(self, client: TestClient):
        """
        Arrange: Client fixture provides fresh app instance
        Act: Call GET /activities
        Assert: Response contains all 9 activities with required fields
        """
        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert len(activities) == 9
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Tennis Club",
            "Art Studio",
            "Music Band",
            "Science Club",
            "Debate Team"
        ]
        assert list(activities.keys()) == expected_activities

    def test_get_activities_returns_activity_details(self, client: TestClient):
        """
        Arrange: Client fixture provides fresh app instance
        Act: Call GET /activities
        Assert: Each activity has required fields (description, schedule, max_participants, participants)
        """
        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity_details in activities.items():
            assert "description" in activity_details
            assert "schedule" in activity_details
            assert "max_participants" in activity_details
            assert "participants" in activity_details
            assert isinstance(activity_details["participants"], list)


class TestSignup:
    """Test suite for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_successful(self, client: TestClient):
        """
        Arrange: Client fixture provides fresh app instance
        Act: Sign up a new student for an activity
        Assert: Response status is 200 and student is added to activity
        """
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert email in response.json().get("message", "")

    def test_signup_adds_student_to_participants(self, client: TestClient):
        """
        Arrange: Client fixture provides fresh app instance
        Act: Sign up a student for an activity
        Assert: Student appears in activity's participants list
        """
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert email in activities[activity_name]["participants"]

    def test_signup_nonexistent_activity_returns_404(self, client: TestClient):
        """
        Arrange: Client fixture provides fresh app instance
        Act: Try to sign up for non-existent activity
        Assert: Response status is 404 with "Activity not found" message
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_signup_duplicate_student_returns_400(self, client: TestClient):
        """
        Arrange: Client fixture provides fresh app instance with student already signed up
        Act: Try to sign up the same student again
        Assert: Response status is 400 with "already signed up" message
        """
        # Arrange
        activity_name = "Chess Club"
        # Use an existing participant from the original data
        email = "michael@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_different_activities_separate_lists(self, client: TestClient):
        """
        Arrange: Client fixture provides fresh app instance
        Act: Sign up same student for different activities
        Assert: Student appears in both activity lists independently
        """
        # Arrange
        email = "newstudent@mergington.edu"
        activity1 = "Chess Club"
        activity2 = "Programming Class"

        # Act
        client.post(f"/activities/{activity1}/signup", params={"email": email})
        client.post(f"/activities/{activity2}/signup", params={"email": email})
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert email in activities[activity1]["participants"]
        assert email in activities[activity2]["participants"]


class TestUnregister:
    """Test suite for POST /activities/{activity_name}/unregister endpoint"""

    def test_unregister_successful(self, client: TestClient):
        """
        Arrange: Client fixture provides fresh app instance with signed-up student
        Act: Unregister student from activity
        Assert: Response status is 200
        """
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        # Sign up first
        client.post(f"/activities/{activity_name}/signup", params={"email": email})

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert email in response.json().get("message", "")

    def test_unregister_removes_student_from_participants(self, client: TestClient):
        """
        Arrange: Client fixture provides fresh app instance with signed-up student
        Act: Unregister student from activity
        Assert: Student is removed from activity's participants list
        """
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        client.post(f"/activities/{activity_name}/signup", params={"email": email})

        # Act
        client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert email not in activities[activity_name]["participants"]

    def test_unregister_nonexistent_activity_returns_404(self, client: TestClient):
        """
        Arrange: Client fixture provides fresh app instance
        Act: Try to unregister from non-existent activity
        Assert: Response status is 404 with "Activity not found" message
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_unregister_not_signed_up_student_returns_400(self, client: TestClient):
        """
        Arrange: Client fixture provides fresh app instance
        Act: Try to unregister a student who is not signed up
        Assert: Response status is 400 with "not signed up" message
        """
        # Arrange
        activity_name = "Chess Club"
        email = "notstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]

    def test_unregister_original_participants_unaffected(self, client: TestClient):
        """
        Arrange: Client fixture provides fresh app instance with original participants
        Act: Unregister a newly signed-up student
        Assert: Original participants remain in the list
        """
        # Arrange
        activity_name = "Chess Club"
        original_participants = ["michael@mergington.edu", "daniel@mergington.edu"]
        email = "newstudent@mergington.edu"
        client.post(f"/activities/{activity_name}/signup", params={"email": email})

        # Act
        client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for original_email in original_participants:
            assert original_email in activities[activity_name]["participants"]
