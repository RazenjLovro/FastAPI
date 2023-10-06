from fastapi import APIRouter, Depends
from app.schemas.user import (
    CreateUsersResponse,
    FullUserProfile,
    MultipleUsersResponse,
    UserProfileInfo,
)
from app.services.user import UserService
import logging
from app.dependecies import rate_limit


logger = logging.getLogger(__name__)


def create_user_router(profile_infos: dict, users_content: dict) -> APIRouter:
    user_router = APIRouter(
        prefix="/user",
        tags=["user"],
        dependencies=[Depends(rate_limit)]
    )
    user_service = UserService(profile_infos, users_content)

    @user_router.get("/all", response_model=MultipleUsersResponse)
    async def get_all_users_paginated(start: int = 0, limit: int = 2):
        users, total = await user_service.get_all_users_with_pagination(start, limit)
        formatted_users = MultipleUsersResponse(users=users, total=total)
        return formatted_users

    @user_router.get("/{user_id}", response_model=FullUserProfile)
    async def get_user_by_id(user_id: int):

        full_user_profile = await user_service.get_user_info(user_id)

        return full_user_profile

    @user_router.put("/{user_id}")
    async def update_user(user_id: int, full_profile_info: FullUserProfile):
        await user_service.create_update_user(full_profile_info, user_id)
        return None

    @user_router.delete("/{user_id}")
    async def remove_user(user_id: int):

        await user_service.delete_user(user_id)

    @user_router.patch("/{user_id}", response_model=FullUserProfile)
    async def patch_user(user_id: int, user_profile_info: UserProfileInfo) -> FullUserProfile:
        await user_service.partial_update_user(user_id, user_profile_info)
        full_user_profile = await user_service.get_user_info(user_id)
        return full_user_profile

    @user_router.post("/", response_model=CreateUsersResponse, status_code=201)
    async def add_user(full_profile_info: FullUserProfile):
        user_id = await user_service.create_update_user(full_profile_info)
        created_user = CreateUsersResponse(user_id=user_id)
        return created_user

    return user_router
