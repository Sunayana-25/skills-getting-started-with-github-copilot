"""
Test cases for the High School Management System API
"""
import pytest


def test_root_redirect(client):
    """Test that root redirects to static index.html"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities(client):
    """Test retrieving all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, dict)
    assert "Soccer Team" in data
    assert "Basketball Club" in data
    assert "Programming Class" in data
    
    # Check structure of one activity
    soccer = data["Soccer Team"]
    assert "description" in soccer
    assert "schedule" in soccer
    assert "max_participants" in soccer
    assert "participants" in soccer
    assert isinstance(soccer["participants"], list)


def test_signup_success(client):
    """Test successful signup for an activity"""
    response = client.post(
        "/activities/Soccer Team/signup",
        params={"email": "newstudent@mergington.edu"}
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "newstudent@mergington.edu" in data["message"]
    assert "Soccer Team" in data["message"]
    
    # Verify student was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "newstudent@mergington.edu" in activities["Soccer Team"]["participants"]


def test_signup_duplicate_student(client):
    """Test that signing up the same student twice fails"""
    email = "duplicate@mergington.edu"
    
    # First signup should succeed
    response1 = client.post(
        "/activities/Soccer Team/signup",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Second signup should fail
    response2 = client.post(
        "/activities/Soccer Team/signup",
        params={"email": email}
    )
    assert response2.status_code == 400
    assert "already signed up" in response2.json()["detail"]


def test_signup_nonexistent_activity(client):
    """Test signup for an activity that doesn't exist"""
    response = client.post(
        "/activities/Nonexistent Activity/signup",
        params={"email": "student@mergington.edu"}
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_full_activity(client):
    """Test signup when activity is at max capacity"""
    # Find Chess Club which has max 12 participants
    activities_response = client.get("/activities")
    activities = activities_response.json()
    chess_club = activities["Chess Club"]
    
    # Fill up the activity to max capacity
    current_count = len(chess_club["participants"])
    spots_available = chess_club["max_participants"] - current_count
    
    for i in range(spots_available):
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": f"student{i}@mergington.edu"}
        )
        assert response.status_code == 200
    
    # Now try to add one more (should fail)
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "overflow@mergington.edu"}
    )
    assert response.status_code == 400
    assert "full" in response.json()["detail"].lower()


def test_unregister_success(client):
    """Test successful unregistration from an activity"""
    # First, sign up a student
    email = "temporary@mergington.edu"
    client.post(
        "/activities/Soccer Team/signup",
        params={"email": email}
    )
    
    # Then unregister
    response = client.post(
        "/activities/Soccer Team/unregister",
        params={"email": email}
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    
    # Verify student was removed
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email not in activities["Soccer Team"]["participants"]


def test_unregister_not_signed_up(client):
    """Test unregistering a student who is not signed up"""
    response = client.post(
        "/activities/Soccer Team/unregister",
        params={"email": "notsignedup@mergington.edu"}
    )
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]


def test_unregister_nonexistent_activity(client):
    """Test unregister from an activity that doesn't exist"""
    response = client.post(
        "/activities/Nonexistent Activity/unregister",
        params={"email": "student@mergington.edu"}
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_existing_participant(client):
    """Test unregistering a participant who was originally in the activity"""
    # Get current participants
    activities_response = client.get("/activities")
    activities = activities_response.json()
    original_participant = activities["Soccer Team"]["participants"][0]
    
    # Unregister them
    response = client.post(
        "/activities/Soccer Team/unregister",
        params={"email": original_participant}
    )
    assert response.status_code == 200
    
    # Verify removal
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert original_participant not in activities["Soccer Team"]["participants"]


def test_multiple_signups_different_activities(client):
    """Test that a student can sign up for multiple activities"""
    email = "multisport@mergington.edu"
    
    # Sign up for Soccer Team
    response1 = client.post(
        "/activities/Soccer Team/signup",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Sign up for Basketball Club
    response2 = client.post(
        "/activities/Basketball Club/signup",
        params={"email": email}
    )
    assert response2.status_code == 200
    
    # Verify student is in both
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities["Soccer Team"]["participants"]
    assert email in activities["Basketball Club"]["participants"]
