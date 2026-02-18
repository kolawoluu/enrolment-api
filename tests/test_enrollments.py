"""Tests for enrollment management endpoints."""


class TestStudentEnrollment:
    def test_enroll_student(self, client, student_user, sample_course):
        response = client.post(
            "/enrollments/",
            json={"user_id": student_user["id"], "course_id": sample_course["id"]},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["user_id"] == student_user["id"]
        assert data["course_id"] == sample_course["id"]

    def test_enroll_duplicate(self, client, student_user, sample_course):
        client.post(
            "/enrollments/",
            json={"user_id": student_user["id"], "course_id": sample_course["id"]},
        )
        response = client.post(
            "/enrollments/",
            json={"user_id": student_user["id"], "course_id": sample_course["id"]},
        )
        assert response.status_code == 400

    def test_enroll_admin_forbidden(self, client, admin_user, sample_course):
        response = client.post(
            "/enrollments/",
            json={"user_id": admin_user["id"], "course_id": sample_course["id"]},
        )
        assert response.status_code == 403

    def test_enroll_nonexistent_student(self, client, sample_course):
        response = client.post(
            "/enrollments/",
            json={"user_id": 999, "course_id": sample_course["id"]},
        )
        assert response.status_code == 404

    def test_enroll_nonexistent_course(self, client, student_user):
        response = client.post(
            "/enrollments/",
            json={"user_id": student_user["id"], "course_id": 999},
        )
        assert response.status_code == 404


class TestStudentDeregistration:
    def test_deregister_student(self, client, student_user, sample_course):
        enroll_resp = client.post(
            "/enrollments/",
            json={"user_id": student_user["id"], "course_id": sample_course["id"]},
        )
        enrollment_id = enroll_resp.json()["id"]

        response = client.delete(
            f"/enrollments/{enrollment_id}",
            params={"user_id": student_user["id"]},
        )
        assert response.status_code == 200

    def test_deregister_nonexistent_enrollment(self, client, student_user):
        response = client.delete(
            "/enrollments/999",
            params={"user_id": student_user["id"]},
        )
        assert response.status_code == 404

    def test_deregister_as_admin_forbidden(self, client, admin_user, student_user, sample_course):
        enroll_resp = client.post(
            "/enrollments/",
            json={"user_id": student_user["id"], "course_id": sample_course["id"]},
        )
        enrollment_id = enroll_resp.json()["id"]

        response = client.delete(
            f"/enrollments/{enrollment_id}",
            params={"user_id": admin_user["id"]},
        )
        assert response.status_code == 403

    def test_deregister_other_students_enrollment(self, client, student_user, sample_course):
    
        resp = client.post(
            "/users/",
            json={"name": "Student Two", "email": "s2@example.com", "role": "student"},
        )
        student2 = resp.json()

        enroll_resp = client.post(
            "/enrollments/",
            json={"user_id": student_user["id"], "course_id": sample_course["id"]},
        )
        enrollment_id = enroll_resp.json()["id"]

        response = client.delete(
            f"/enrollments/{enrollment_id}",
            params={"user_id": student2["id"]},
        )
        assert response.status_code == 403


class TestGetStudentEnrollments:
    def test_get_student_enrollments(self, client, student_user, sample_course, admin_user):
        client.post(
            "/enrollments/",
            json={"user_id": student_user["id"], "course_id": sample_course["id"]},
        )

        course2 = client.post(
            "/courses/",
            json={"title": "Algorithms", "code": "CS202"},
            params={"user_id": admin_user["id"]},
        ).json()
        client.post(
            "/enrollments/",
            json={"user_id": student_user["id"], "course_id": course2["id"]},
        )

        response = client.get(f"/enrollments/student/{student_user['id']}")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_get_student_enrollments_empty(self, client, student_user):
        response = client.get(f"/enrollments/student/{student_user['id']}")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_enrollments_nonexistent_student(self, client):
        response = client.get("/enrollments/student/999")
        assert response.status_code == 404


class TestAdminEnrollmentOversight:
    def test_get_all_enrollments(self, client, admin_user, student_user, sample_course):
        client.post(
            "/enrollments/",
            json={"user_id": student_user["id"], "course_id": sample_course["id"]},
        )
        response = client.get("/enrollments/", params={"user_id": admin_user["id"]})
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_get_all_enrollments_as_student_forbidden(self, client, student_user):
        response = client.get("/enrollments/", params={"user_id": student_user["id"]})
        assert response.status_code == 403

    def test_get_course_enrollments(self, client, admin_user, student_user, sample_course):
        client.post(
            "/enrollments/",
            json={"user_id": student_user["id"], "course_id": sample_course["id"]},
        )
        response = client.get(
            f"/enrollments/course/{sample_course['id']}",
            params={"user_id": admin_user["id"]},
        )
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_get_course_enrollments_as_student_forbidden(self, client, student_user, sample_course):
        response = client.get(
            f"/enrollments/course/{sample_course['id']}",
            params={"user_id": student_user["id"]},
        )
        assert response.status_code == 403

    def test_get_course_enrollments_nonexistent_course(self, client, admin_user):
        response = client.get(
            "/enrollments/course/999",
            params={"user_id": admin_user["id"]},
        )
        assert response.status_code == 404

    def test_admin_force_deregister(self, client, admin_user, student_user, sample_course):
        enroll_resp = client.post(
            "/enrollments/",
            json={"user_id": student_user["id"], "course_id": sample_course["id"]},
        )
        enrollment_id = enroll_resp.json()["id"]

        response = client.delete(
            f"/enrollments/admin/{enrollment_id}",
            params={"user_id": admin_user["id"]},
        )
        assert response.status_code == 200


        all_enrollments = client.get("/enrollments/", params={"user_id": admin_user["id"]})
        assert len(all_enrollments.json()) == 0

    def test_admin_force_deregister_as_student_forbidden(self, client, student_user, sample_course):
        enroll_resp = client.post(
            "/enrollments/",
            json={"user_id": student_user["id"], "course_id": sample_course["id"]},
        )
        enrollment_id = enroll_resp.json()["id"]

        response = client.delete(
            f"/enrollments/admin/{enrollment_id}",
            params={"user_id": student_user["id"]},
        )
        assert response.status_code == 403

    def test_admin_force_deregister_nonexistent(self, client, admin_user):
        response = client.delete(
            "/enrollments/admin/999",
            params={"user_id": admin_user["id"]},
        )
        assert response.status_code == 404
