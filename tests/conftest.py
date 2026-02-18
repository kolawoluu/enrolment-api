"""Shared test fixtures."""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.data.store import reset_store


@pytest.fixture(autouse=True)
def clean_store():
    """Reset the in-memory store before each test."""
    reset_store()
    yield
    reset_store()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def admin_user(client):
    """Create and return an admin user."""
    response = client.post("/users/", json={"name": "Admin User", "email": "admin@example.com", "role": "admin"})
    return response.json()


@pytest.fixture
def student_user(client):
    """Create and return a student user."""
    response = client.post("/users/", json={"name": "Student User", "email": "student@example.com", "role": "student"})
    return response.json()


@pytest.fixture
def sample_course(client, admin_user):
    """Create and return a sample course."""
    response = client.post(
        "/courses/",
        json={"title": "Introduction to Python", "code": "CS101"},
        params={"user_id": admin_user["id"]},
    )
    return response.json()
