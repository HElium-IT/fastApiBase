from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.tests.utils.utils import random_email, random_lower_string
from app.core.security import verify_password


def user_authentication_headers(
    *, client: TestClient, email: str, password: str
) -> Dict[str, str]:
    data = {"username": email, "password": password}

    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    response = r.json()
    print(f"data: {data}\n response: {r}\n response.json: {response}")
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers

def create_random_user(db: Session) -> User:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(username=email, email=email, password=password)
    user = crud.user.create(db=db, obj_in=user_in)
    return user


def authentication_token_for_user(
    *, client: TestClient, db: Session
) -> Dict[str, str]:
    """
    Return a valid token for the user with given email.

    If the user doesn't exist it is created first.
    """
    
    user = crud.user.get_by_email(db, email=settings.EMAIL_TEST_USER)
    if user is None:
        print("creating test user")
        user_in_create = UserCreate(email=settings.EMAIL_TEST_USER, password=settings.PASSWORD_TEST_USER)
        user = crud.user.create(db, obj_in=user_in_create)
    else:
        print("updating test user")
        user_in_update = UserUpdate(password=settings.PASSWORD_TEST_USER)
        user = crud.user.update(db, db_obj=user, obj_in=user_in_update)
    
    db.commit()
    print(f"testingUser: {crud.user.get(db=db, id=user.id).__dict__}")
    return user_authentication_headers(client=client, email=settings.EMAIL_TEST_USER, password=settings.PASSWORD_TEST_USER)


def authentication_token_for_super_user(
    *, client: TestClient, db: Session
) -> Dict[str, str]:
    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if user is None:
        print("creating test superUser")
        user_in_create = UserCreate(email=settings.FIRST_SUPERUSER, password=settings.FIRST_SUPERUSER_PASSWORD, is_superuser=True)
        user = crud.user.create(db, obj_in=user_in_create)
        db.commit()
    
    print(f"testingSuperUser: {user.__dict__}")
    return user_authentication_headers(
        client=client, email=settings.FIRST_SUPERUSER, password=settings.FIRST_SUPERUSER_PASSWORD
    )