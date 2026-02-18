"""Pydantic models for request validation and response schemas."""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator


class RoleEnum(str, Enum):
    student = "student"
    admin = "admin"


# User Models 

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    role: RoleEnum

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("name must not be empty")
        return v.strip()


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: RoleEnum


# Course Models 

class CourseCreate(BaseModel):
    title: str
    code: str

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("title must not be empty")
        return v.strip()

    @field_validator("code")
    @classmethod
    def code_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("code must not be empty")
        return v.strip()


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    code: Optional[str] = None

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("title must not be empty")
        return v.strip() if v else v

    @field_validator("code")
    @classmethod
    def code_not_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("code must not be empty")
        return v.strip() if v else v


class CourseResponse(BaseModel):
    id: int
    title: str
    code: str


# Enrollment Models 

class EnrollmentCreate(BaseModel):
    user_id: int
    course_id: int


class EnrollmentResponse(BaseModel):
    id: int
    user_id: int
    course_id: int
