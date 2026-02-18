"""Course management endpoints with role-based access."""

from typing import Optional
from fastapi import APIRouter, HTTPException, Query, status

from app.data.store import courses, users, get_next_course_id
from app.models.schemas import CourseCreate, CourseUpdate, CourseResponse

router = APIRouter(prefix="/courses", tags=["Courses"])


def _verify_admin(user_id: int):
    """Verify that the given user exists and is an admin."""
    if user_id not in users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if users[user_id]["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can perform this action")


def _check_code_unique(code: str, exclude_id: Optional[int] = None):
    """Ensure course code is unique."""
    for cid, course in courses.items():
        if course["code"] == code and cid != exclude_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Course code already exists",
            )


# ── Public endpoints ─────────────────────────────────────────────────────────

@router.get("/", response_model=list[CourseResponse])
def get_all_courses():
    """Retrieve all courses (public)."""
    return list(courses.values())


@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: int):
    """Retrieve a course by ID (public)."""
    if course_id not in courses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return courses[course_id]


# ── Admin-only endpoints ─────────────────────────────────────────────────────

@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(course: CourseCreate, user_id: int = Query(..., description="ID of the admin user")):
    """Create a new course (admin only)."""
    _verify_admin(user_id)
    _check_code_unique(course.code)
    course_id = get_next_course_id()
    course_data = {"id": course_id, "title": course.title, "code": course.code}
    courses[course_id] = course_data
    return course_data


@router.put("/{course_id}", response_model=CourseResponse)
def update_course(
    course_id: int,
    course: CourseUpdate,
    user_id: int = Query(..., description="ID of the admin user"),
):
    """Update a course (admin only)."""
    _verify_admin(user_id)
    if course_id not in courses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    existing = courses[course_id]
    if course.title is not None:
        existing["title"] = course.title
    if course.code is not None:
        _check_code_unique(course.code, exclude_id=course_id)
        existing["code"] = course.code
    return existing


@router.delete("/{course_id}", status_code=status.HTTP_200_OK)
def delete_course(
    course_id: int,
    user_id: int = Query(..., description="ID of the admin user"),
):
    """Delete a course (admin only)."""
    _verify_admin(user_id)
    if course_id not in courses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    del courses[course_id]
    return {"detail": "Course deleted successfully"}
