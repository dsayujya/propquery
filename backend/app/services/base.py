"""Generic service layer for standard CRUD operations."""

from typing import Generic, List, TypeVar, Optional, Any
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.repositories.base import CRUDBase
from app.utils.exceptions import NotFoundException
from app.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class ServiceBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, repository: CRUDBase[ModelType, CreateSchemaType, UpdateSchemaType], entity_name: str = "Resource"):
        self.repo = repository
        self.entity_name = entity_name

    def get(self, db: Session, id: Any) -> ModelType:
        obj = self.repo.get(db, id=id)
        if not obj:
            raise NotFoundException(detail=f"{self.entity_name} not found")
        return obj

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return self.repo.get_multi(db, skip=skip, limit=limit)

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        return self.repo.create(db, obj_in=obj_in)

    def update(self, db: Session, id: Any, obj_in: UpdateSchemaType) -> ModelType:
        db_obj = self.get(db, id=id)
        return self.repo.update(db, db_obj=db_obj, obj_in=obj_in)

    def remove(self, db: Session, id: Any) -> ModelType:
        self.get(db, id=id) # ensure it exists
        return self.repo.remove(db, id=id)

