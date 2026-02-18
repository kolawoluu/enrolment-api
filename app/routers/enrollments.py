"""Enrollment management endpoints."""

from fastapi import APIRouter, HTTPException, Query, status

from app.data.store import enrollments, users, courses, get_next_enrollment_id
from app.models.schemas import EnrollmentCreate, EnrollmentResponse

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])


def _verify_student(user_id: int):
    """Verify that the user exists and is a student."""
    if user_id not in users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if users[user_id]["role"] != "student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can enroll or deregister",
        )


def _verify_admin(user_id: int):
    """Verify that the user exists and is an admin."""
    if user_id not in users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if users[user_id]["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can perform this action")


# ── Student Enrollment ───────────────────────────────────────────────────────

@router.post("/", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def enroll_student(enrollment: EnrollmentCreate):
    """Enroll a student in a course."""
    _verify_student(enrollment.user_id)

    if enrollment.course_id not in courses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    # Check duplicate enrollment
    for e in enrollments.values():
        if e["user_id"] == enrollment.user_id and e["course_id"] == enrollment.course_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student is already enrolled in this course",
            )

    enrollment_id = get_next_enrollment_id()
    enrollment_data = {
        "id": enrollment_id,
        "user_id": enrollment.user_id,
        "course_id": enrollment.course_id,
    }
    enrollments[enrollment_id] = enrollment_data
    return enrollment_data


@router.delete("/{enrollment_id}", status_code=status.HTTP_200_OK)
def deregister_student(
    enrollment_id: int,
    user_id: int = Query(..., description="ID of the student"),
):
    """Deregister a student from a course."""
    _verify_student(user_id)

    if enrollment_id not in enrollments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found")

    enrollment = enrollments[enrollment_id]
    if enrollment["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Students can only deregister their own enrollments",
        )

    del enrollments[enrollment_id]
    return {"detail": "Successfully deregistered from course"}


@router.get("/student/{student_id}", response_model=list[EnrollmentResponse])
def get_student_enrollments(student_id: int):
    """Retrieve all enrollments for a specific student."""
    if student_id not in users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return [e for e in enrollments.values() if e["user_id"] == student_id]


# ── Admin Enrollment Oversight ───────────────────────────────────────────────

@router.get("/", response_model=list[EnrollmentResponse])
def get_all_enrollments(user_id: int = Query(..., description="ID of the admin user")):
    """Retrieve all enrollments (admin only)."""
    _verify_admin(user_id)
    return list(enrollments.values())


@router.get("/course/{course_id}", response_model=list[EnrollmentResponse])
def get_course_enrollments(
    course_id: int,
    user_id: int = Query(..., description="ID of the admin user"),
):
    """Retrieve all enrollments for a specific course (admin only)."""
    _verify_admin(user_id)
    if course_id not in courses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return [e for e in enrollments.values() if e["course_id"] == course_id]


@router.delete("/admin/{enrollment_id}", status_code=status.HTTP_200_OK)
def admin_force_deregister(
    enrollment_id: int,
    user_id: int = Query(..., description="ID of the admin user"),
):
    """Force deregister a student from a course (admin only)."""
    _verify_admin(user_id)
    if enrollment_id not in enrollments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found")
    del enrollments[enrollment_id]
    return {"detail": "Student force-deregistered from course"}
