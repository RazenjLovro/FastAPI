import pytest
from app.services.user import UserService


@pytest.fixture
def profile_infos():
    val = {
        0: {
            "short_description": "My bio description",
            "long_bio": "This is our longer bio"
        }
    }
    return val


@pytest.fixture
def users_content():
    val = {
        0: {
            "username": "some name",
            "liked_posts": [1] * 9
        },
    }
    return val


@pytest.fixture
def user_service(profile_infos, users_content):
    user_service = UserService(profile_infos, users_content)
    return user_service



