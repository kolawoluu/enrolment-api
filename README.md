# Course Enrollment Management API

A RESTful API built with **FastAPI** that manages a course enrollment system with role-based access control (student and admin roles), using in-memory data storage.

## Project Structure

```
course-enrollment-api/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI application entry point
│   ├── data/
│   │   ├── __init__.py
│   │   └── store.py             # In-memory data store
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py           # Pydantic models for validation
│   └── routers/
│       ├── __init__.py
│       ├── users.py             # User management endpoints
│       ├── courses.py           # Course endpoints (public + admin)
│       └── enrollments.py       # Enrollment endpoints (student + admin)
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Shared test fixtures
│   ├── test_users.py            # User endpoint tests
│   ├── test_courses.py          # Course endpoint tests
│   └── test_enrollments.py      # Enrollment endpoint tests
├── requirements.txt
└── README.md
```

## Setup

### 1. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

## How to Run the API

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

Interactive API documentation is at `http://127.0.0.1:8000/docs`.

## How to Run the Tests

```bash
pytest tests/ -v
```

To run with coverage (install `pytest-cov` first):

```bash
pytest tests/ -v --cov=app --cov-report=term-missing
```

## API Endpoints

### Users

| Method | Endpoint        | Description        | Access  |
|--------|-----------------|--------------------|---------|
| POST   | `/users/`       | Create a user      | Public  |
| GET    | `/users/`       | Get all users      | Public  |
| GET    | `/users/{id}`   | Get user by ID     | Public  |

### Courses

| Method | Endpoint            | Description        | Access     |
|--------|---------------------|--------------------|------------|
| GET    | `/courses/`         | Get all courses    | Public     |
| GET    | `/courses/{id}`     | Get course by ID   | Public     |
| POST   | `/courses/`         | Create a course    | Admin only |
| PUT    | `/courses/{id}`     | Update a course    | Admin only |
| DELETE | `/courses/{id}`     | Delete a course    | Admin only |

Admin endpoints require a `user_id` query parameter identifying the admin user.

### Enrollments

| Method | Endpoint                        | Description                      | Access       |
|--------|---------------------------------|----------------------------------|--------------|
| POST   | `/enrollments/`                 | Enroll in a course               | Student only |
| DELETE | `/enrollments/{id}`             | Deregister from a course         | Student only |
| GET    | `/enrollments/student/{id}`     | Get enrollments for a student    | Public       |
| GET    | `/enrollments/`                 | Get all enrollments              | Admin only   |
| GET    | `/enrollments/course/{id}`      | Get enrollments for a course     | Admin only   |
| DELETE | `/enrollments/admin/{id}`       | Force deregister a student       | Admin only   |

## Role-Based Access

- **Admin role** is passed via the `user_id` query parameter for admin-only operations
- **Student role** is determined from the `user_id` field in the request body (enrollments) or query parameter (deregistration)
- No authentication is required; the system trusts the provided user identity
