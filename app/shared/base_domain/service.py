from typing import Generic, TypeVar
from uuid import UUID
from pydantic import BaseModel
from sqlmodel import Session
from app.shared.base_domain.model import BaseTable
from app.shared.base_domain.repository import IBaseRepository, BaseRepository
from app.shared.exceptions import NotFoundException
from app.shared.pagination import PageResponse
from abc import ABC, abstractmethod

T = TypeVar("T", bound=BaseTable)


class IBaseService(ABC, Generic[T]):
    entity_name: str

    @abstractmethod
    def get_by_id(self, id: UUID) -> T:
        raise NotImplementedError

    @abstractmethod
    def get_all(self, offset: int = 0, limit: int = 20) -> PageResponse[T]:
        raise NotImplementedError

    @abstractmethod
    def create_entity(self, payload: BaseModel) -> T:
        raise NotImplementedError

    @abstractmethod
    def update_entity(self, id: UUID, payload: BaseModel) -> T:
        raise NotImplementedError

    @abstractmethod
    def delete_entity(self, id: UUID) -> bool:
        raise NotImplementedError


class BaseService(IBaseService[T], Generic[T]):
    entity_name: str = "Entidad"
    repository_class: type[BaseRepository] = None

    def __init__(self, session: Session):
        self.repository: IBaseRepository[T] = self.repository_class(session)

    def get_by_id(self, id: UUID) -> T:
        entity = self.repository.get_by_id(id)
        if not entity:
            raise NotFoundException(self.entity_name, id)
        return entity

    def get_all(self, offset: int = 0, limit: int = 20) -> PageResponse[T]:
        items, total = self.repository.get_all(offset, limit)
        return PageResponse(total=total, offset=offset, limit=limit, data=items)

    def create_entity(self, payload: BaseModel) -> T:
        return self.repository.create(self._build_entity(payload))

    def update_entity(self, id: UUID, payload: BaseModel) -> T:
        entity = self.get_by_id(id)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(entity, field, value)
        return self.repository.update(entity)

    def delete_entity(self, id: UUID) -> bool:
        entity = self.repository.get_by_id(id)
        if not entity:
            return False
        self.repository.delete(entity)
        return True

    def _build_entity(self, payload: BaseModel) -> T:
        return self.repository.model(**payload.model_dump())
