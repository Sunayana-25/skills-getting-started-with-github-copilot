"""
Pytest configuration and fixtures
"""
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Create a test client"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to initial state before each test"""
    # Store original state
    original_activities = {
        "Soccer Team": {
            "id": "soccer-team",
            "category": "sports",
            "description": "Join the varsity soccer team and compete in regional tournaments",
            "schedule": "Mondays, Wednesdays, Fridays, 4:00 PM - 6:00 PM",
            "max_participants": 25,
            "participants": ["alex@mergington.edu", "sarah@mergington.edu"]
        },
        "Basketball Club": {
            "id": "basketball-club",
            "category": "sports",
            "description": "Practice basketball skills and participate in friendly matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 20,
            "participants": ["james@mergington.edu", "emily@mergington.edu"]
        },
        "Art Studio": {
            "id": "art-studio",
            "category": "artistic",
            "description": "Explore various art mediums including painting, drawing, and sculpture",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 15,
            "participants": ["lily@mergington.edu", "noah@mergington.edu"]
        },
        "Drama Club": {
            "id": "drama-club",
            "category": "artistic",
            "description": "Participate in theatrical productions and develop acting skills",
            "schedule": "Mondays and Thursdays, 3:30 PM - 5:30 PM",
            "max_participants": 30,
            "participants": ["ava@mergington.edu", "liam@mergington.edu"]
        },
        "Debate Team": {
            "id": "debate-team",
            "category": "intellectual",
            "description": "Develop critical thinking and public speaking through competitive debates",
            "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["mia@mergington.edu", "ethan@mergington.edu"]
        },
        "Science Olympiad": {
            "id": "science-olympiad",
            "category": "intellectual",
            "description": "Compete in science competitions and conduct research projects",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["isabella@mergington.edu", "mason@mergington.edu"]
        },
        "Chess Club": {
            "id": "chess-club",
            "category": "intellectual",
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        }
    }
    
    # Reset before test
    activities.clear()
    activities.update(original_activities)
    
    yield
    
    # Reset after test
    activities.clear()
    activities.update(original_activities)
