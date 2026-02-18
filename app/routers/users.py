"""User management endpoints."""

from fastapi import APIRouter, HTTPException, status

from app.data.store import users, get_next_user_id
from app.models.schemas import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    """Create a new user."""
    user_id = get_next_user_id()
    user_data = {"id": user_id, "name": user.name, "email": user.email, "role": user.role.value}
    users[user_id] = user_data
    return user_data


@router.get("/", response_model=list[UserResponse])
def get_all_users():
    """Retrieve all users."""
    return list(users.values())


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    """Retrieve a user by ID."""
    if user_id not in users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return users[user_id]
