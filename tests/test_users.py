"""Tests for user management endpoints."""


class TestCreateUser:
    def test_create_student(self, client):
        response = client.post("/users/", json={"name": "Alice", "email": "alice@example.com", "role": "student"})
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Alice"
        assert data["email"] == "alice@example.com"
        assert data["role"] == "student"
        assert "id" in data

    def test_create_admin(self, client):
        response = client.post("/users/", json={"name": "Bob", "email": "bob@example.com", "role": "admin"})
        assert response.status_code == 201
        assert response.json()["role"] == "admin"

    def test_create_user_empty_name(self, client):
        response = client.post("/users/", json={"name": "", "email": "test@example.com", "role": "student"})
        assert response.status_code == 422

    def test_create_user_whitespace_name(self, client):
        response = client.post("/users/", json={"name": "   ", "email": "test@example.com", "role": "student"})
        assert response.status_code == 422

    def test_create_user_invalid_email(self, client):
        response = client.post("/users/", json={"name": "Alice", "email": "not-an-email", "role": "student"})
        assert response.status_code == 422

    def test_create_user_invalid_role(self, client):
        response = client.post("/users/", json={"name": "Alice", "email": "alice@example.com", "role": "teacher"})
        assert response.status_code == 422


class TestGetUsers:
    def test_get_all_users_empty(self, client):
        response = client.get("/users/")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_all_users(self, client, admin_user, student_user):
        response = client.get("/users/")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_get_user_by_id(self, client, student_user):
        response = client.get(f"/users/{student_user['id']}")
        assert response.status_code == 200
        assert response.json()["name"] == "Student User"

    def test_get_user_not_found(self, client):
        response = client.get("/users/999")
        assert response.status_code == 404
