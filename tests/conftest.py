"""
Pytest configuration and shared fixtures for API tests.

Provides fixtures for isolated app instances with fresh data per test.
"""

import pytest
from fastapi.testclient import TestClient
from copy import deepcopy
from src.app import app, activities


# Store the original activities data
ORIGINAL_ACTIVITIES = deepcopy(activities)


@pytest.fixture
def client():
    """
    Fixture that provides a TestClient with a fresh copy of app data.
    
    Arrange: Reset activities to original state before each test
    Returns: TestClient instance configured with the app
    """
    # Reset activities to original state for test isolation
    activities.clear()
    activities.update(deepcopy(ORIGINAL_ACTIVITIES))
    
    # Provide the test client
    return TestClient(app)
