from abc import ABC
from typing import Type, TypeVar
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from app.shared.base_domain.service import IBaseService
from app.shared.pagination import PageParams, PageResponse

S = TypeVar("S", bound=IBaseService)


class BaseApiController(ABC):
    service_dep: S
    response_schema: Type[BaseModel]
    create_schema: Type[BaseModel] | None = None
    update_schema: Type[BaseModel] | None = None
    prefix: str
    tags: list[str] | None = None

    def __init__(self):
        self.router = APIRouter(
            prefix=self.prefix,
            tags=self.tags or [self.prefix.strip("/").title()],
        )
        self._register_routes()

    def _register_routes(self):
        pass


class ReadOnlyApiController(BaseApiController):
    def _register_routes(self):

        def list(service: self.service_dep, page: PageParams = Depends()):
            return service.get_all(offset=page.offset, limit=page.limit)

        self.router.add_api_route(
            "/",
            list,
            methods=["GET"],
            response_model=PageResponse[self.response_schema],
        )

        def retrieve(service: self.service_dep, resource_id: UUID):
            return service.get_by_id(resource_id)

        self.router.add_api_route(
            "/{resource_id}",
            retrieve,
            methods=["GET"],
            response_model=self.response_schema,
        )


class ImmutableApiController(ReadOnlyApiController):
    def _register_routes(self):
        super()._register_routes()

        def create(service: self.service_dep, payload: self.create_schema):
            return service.create_entity(payload)

        self.router.add_api_route(
            "/",
            create,
            methods=["POST"],
            response_model=self.response_schema,
            status_code=status.HTTP_201_CREATED,
        )


class FullCrudApiController(ImmutableApiController):
    def _register_routes(self):
        super()._register_routes()

        def update(
            service: self.service_dep,
            resource_id: UUID,
            payload: self.update_schema,
        ):
            return service.update_entity(resource_id, payload)

        self.router.add_api_route(
            "/{resource_id}",
            update,
            methods=["PATCH"],
            response_model=self.response_schema,
        )

        def delete(service: self.service_dep, resource_id: UUID):
            if not service.delete_entity(resource_id):
                raise HTTPException(status.HTTP_404_NOT_FOUND, "Recurso no encontrado")

        self.router.add_api_route(
            "/{resource_id}",
            delete,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
