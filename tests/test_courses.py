"""Tests for course management endpoints."""


class TestPublicCourseAccess:
    def test_get_all_courses_empty(self, client):
        response = client.get("/courses/")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_all_courses(self, client, sample_course):
        response = client.get("/courses/")
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_get_course_by_id(self, client, sample_course):
        response = client.get(f"/courses/{sample_course['id']}")
        assert response.status_code == 200
        assert response.json()["title"] == "Introduction to Python"
        assert response.json()["code"] == "CS101"

    def test_get_course_not_found(self, client):
        response = client.get("/courses/999")
        assert response.status_code == 404


class TestAdminCourseCreation:
    def test_create_course_as_admin(self, client, admin_user):
        response = client.post(
            "/courses/",
            json={"title": "Data Structures", "code": "CS201"},
            params={"user_id": admin_user["id"]},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Data Structures"
        assert data["code"] == "CS201"

    def test_create_course_as_student_forbidden(self, client, student_user):
        response = client.post(
            "/courses/",
            json={"title": "Data Structures", "code": "CS201"},
            params={"user_id": student_user["id"]},
        )
        assert response.status_code == 403

    def test_create_course_duplicate_code(self, client, admin_user, sample_course):
        response = client.post(
            "/courses/",
            json={"title": "Another Course", "code": "CS101"},
            params={"user_id": admin_user["id"]},
        )
        assert response.status_code == 400

    def test_create_course_empty_title(self, client, admin_user):
        response = client.post(
            "/courses/",
            json={"title": "", "code": "CS201"},
            params={"user_id": admin_user["id"]},
        )
        assert response.status_code == 422

    def test_create_course_empty_code(self, client, admin_user):
        response = client.post(
            "/courses/",
            json={"title": "Valid Title", "code": ""},
            params={"user_id": admin_user["id"]},
        )
        assert response.status_code == 422

    def test_create_course_nonexistent_user(self, client):
        response = client.post(
            "/courses/",
            json={"title": "Course", "code": "CS301"},
            params={"user_id": 999},
        )
        assert response.status_code == 404


class TestAdminCourseUpdate:
    def test_update_course_title(self, client, admin_user, sample_course):
        response = client.put(
            f"/courses/{sample_course['id']}",
            json={"title": "Advanced Python"},
            params={"user_id": admin_user["id"]},
        )
        assert response.status_code == 200
        assert response.json()["title"] == "Advanced Python"
        assert response.json()["code"] == "CS101"  

    def test_update_course_code(self, client, admin_user, sample_course):
        response = client.put(
            f"/courses/{sample_course['id']}",
            json={"code": "CS102"},
            params={"user_id": admin_user["id"]},
        )
        assert response.status_code == 200
        assert response.json()["code"] == "CS102"

    def test_update_course_duplicate_code(self, client, admin_user, sample_course):

        client.post(
            "/courses/",
            json={"title": "Second Course", "code": "CS202"},
            params={"user_id": admin_user["id"]},
        )

        response = client.put(
            f"/courses/{sample_course['id']}",
            json={"code": "CS202"},
            params={"user_id": admin_user["id"]},
        )
        assert response.status_code == 400

    def test_update_course_as_student_forbidden(self, client, student_user, sample_course):
        response = client.put(
            f"/courses/{sample_course['id']}",
            json={"title": "Hacked"},
            params={"user_id": student_user["id"]},
        )
        assert response.status_code == 403

    def test_update_course_not_found(self, client, admin_user):
        response = client.put(
            "/courses/999",
            json={"title": "Doesn't Exist"},
            params={"user_id": admin_user["id"]},
        )
        assert response.status_code == 404


class TestAdminCourseDelete:
    def test_delete_course(self, client, admin_user, sample_course):
        response = client.delete(
            f"/courses/{sample_course['id']}",
            params={"user_id": admin_user["id"]},
        )
        assert response.status_code == 200
        assert client.get(f"/courses/{sample_course['id']}").status_code == 404

    def test_delete_course_as_student_forbidden(self, client, student_user, sample_course):
        response = client.delete(
            f"/courses/{sample_course['id']}",
            params={"user_id": student_user["id"]},
        )
        assert response.status_code == 403

    def test_delete_course_not_found(self, client, admin_user):
        response = client.delete("/courses/999", params={"user_id": admin_user["id"]})
        assert response.status_code == 404
