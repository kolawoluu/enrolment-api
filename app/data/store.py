"""In-memory data store for users, courses, and enrollments."""

# Data stores
users: dict[int, dict] = {}
courses: dict[int, dict] = {}
enrollments: dict[int, dict] = {}

# Auto-increment counters
user_id_counter: int = 0
course_id_counter: int = 0
enrollment_id_counter: int = 0


def get_next_user_id() -> int:
    global user_id_counter
    user_id_counter += 1
    return user_id_counter


def get_next_course_id() -> int:
    global course_id_counter
    course_id_counter += 1
    return course_id_counter


def get_next_enrollment_id() -> int:
    global enrollment_id_counter
    enrollment_id_counter += 1
    return enrollment_id_counter


def reset_store():
    """Reset all data stores. Used in tests."""
    global user_id_counter, course_id_counter, enrollment_id_counter
    users.clear()
    courses.clear()
    enrollments.clear()
    user_id_counter = 0
    course_id_counter = 0
    enrollment_id_counter = 0
