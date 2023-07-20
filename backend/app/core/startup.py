from logging import Logger
from app import crud, schemas
from app.core.config import settings
from app.dependencies import get_db

logger = Logger(__name__)


def startup():
    print("Running startup functions")
    create_first_super_user()


def create_first_super_user():
    db = next(get_db())
    super_user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if super_user:
        print(f"Superuser {super_user.email} already exists")
    else:
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.user.create(db, obj_in=user_in)
        db.commit()
        print(f"Created first superuser: {user.email} - {user.id}")
