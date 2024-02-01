from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

if TYPE_CHECKING:
    from webapp.schema.education.course import CourseRead


class User(BaseModel):
    id: int = Field(..., example=1)
    username: str = Field(..., example='user')
    email: EmailStr = Field(..., example='user@example.com')
    role: Optional[str] = Field(None, example='admin')
    additional_info: Optional[dict] = Field(None, example={'full_name': 'Дмитрий Петров'})

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    username: str = Field(..., example='user123')
    password: str = Field(..., example='strongpassword')


class UserLoginResponse(BaseModel):
    access_token: str = Field(
        ...,
        example='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c',
    )


class UserCreate(User):
    password: str = Field(..., example='newpassword')


class UserRead(User):
    subscribed_courses: Optional[List[CourseRead]] = []

    model_config = ConfigDict(from_attributes=True)
