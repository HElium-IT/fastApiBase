
# create a decorator that will commit the session after the function is executed
# and rollback if an exception is raised

from functools import wraps
from sqlalchemy.exc import SQLAlchemyError

def db_commit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            kwargs.get('db').commit()
            return result
        except SQLAlchemyError as e:
            kwargs.get('db').rollback()
            raise e
    return wrapper
    

