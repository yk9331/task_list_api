import functools
import inspect

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.config import settings

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    **settings.SQLALCHEMY_ENGINE_OPTIONS,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def managed_transaction(func):
    """
    wrap request in single transation
    """

    @functools.wraps(func)
    async def wrapper(*args, db: Session = Depends(get_db), **kwargs):
        try:
            if inspect.iscoroutinefunction(func):
                result = await func(*args, db=db, **kwargs)
            else:
                result = func(*args, db=db, **kwargs)
            db.commit()
            return result
        except Exception:
            db.rollback()
            raise

    return wrapper
