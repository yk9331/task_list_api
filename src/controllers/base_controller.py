from typing import Any, Dict, Generic, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import src.core.error_msg as error_msg
import src.core.exceptions as exc
from src.core.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseController(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(
        self,
        model: Type[ModelType],
        *,
        not_found_msg: str = error_msg.NOT_FOUND_DEFAULT
    ):
        """
        Controller with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `not_found_msg`: A message to return when the object is not found
        """
        self.model = model
        self.not_found_msg = not_found_msg

    def get_all(self, db: Session) -> Optional[ModelType]:
        return db.scalars(select(self.model)).all()

    def get_by_id(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.get(self.model, id)

    def get_by_id_or_404(self, db: Session, id: Any) -> Optional[ModelType]:
        db_obj = db.get(self.model, id)
        if not db_obj:
            raise exc.NotFoundError(self.not_found_msg)
        return db_obj

    def get_by_id_for_update(self, db: Session, id: Any) -> Optional[ModelType]:
        db_obj = db.scalars(
            select(self.model).filter_by(id=id).with_for_update()
        ).first()
        if not db_obj:
            raise exc.NotFoundError(self.not_found_msg)
        return db_obj

    def get_by_filter(self, db: Session, **kwargs) -> Optional[ModelType]:
        return db.scalars(select(self.model).filter_by(**kwargs)).first()

    def get_by_filter_or_404(self, db: Session, **kwargs) -> Optional[ModelType]:
        db_obj = db.scalars(select(self.model).filter_by(**kwargs)).first()
        if not db_obj:
            raise exc.NotFoundError(self.not_found_msg)
        return db_obj

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        try:
            create_data = jsonable_encoder(
                obj_in,
                by_alias=False,
            )
            db_obj = self.model(**create_data)
            db.add(db_obj)
            db.flush()
            db.refresh(db_obj)
            return db_obj
        except IntegrityError:
            raise exc.ConflictError()

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        try:
            obj_data = jsonable_encoder(db_obj)
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = jsonable_encoder(
                    obj_in,
                    exclude_unset=True,
                    by_alias=False,
                )
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            db.add(db_obj)
            db.flush()
            db.refresh(db_obj)
            return db_obj
        except IntegrityError:
            raise exc.ConflictError()

    def update_by_id(
        self, db: Session, *, id: Any, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        db_obj = self.get_by_id_for_update(db, id)
        return self.update(db, db_obj=db_obj, obj_in=obj_in)

    def remove_by_id(self, db: Session, *, id: int) -> ModelType:
        db_obj = self.get_by_id_for_update(db, id)
        db.delete(db_obj)
        db.flush()
        return db_obj
