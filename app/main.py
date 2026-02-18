"""Course Enrollment Management API - Main Application."""

from fastapi import FastAPI

from app.routers import users, courses, enrollments

app = FastAPI(
    title="Course Enrollment Management API",
    description="A RESTful API for managing course enrollments with role-based access control.",
    version="1.0.0",
)

app.include_router(users.router)
app.include_router(courses.router)
app.include_router(enrollments.router)


@app.get("/")
def root():
    return {"Course Enrollment Management API"}
