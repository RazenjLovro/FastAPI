from pydantic import BaseModel, Field
from typing import Optional


class User(BaseModel):
    username: str = Field(
        alias="name",
        title="The Username",
        description="This is the username of the user",
        min_length=1,
        default=None
    )
    liked_posts: Optional[list[int]] = Field(
        description="Array of post ids the user liked",
    )


class UserProfileInfo(BaseModel):
    short_description: str
    long_bio: str


class FullUserProfile(UserProfileInfo, User):
    pass


class MultipleUsersResponse(BaseModel):
    users: list[FullUserProfile]
    total: int


class CreateUsersResponse(BaseModel):
    user_id: int
