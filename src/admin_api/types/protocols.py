from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Protocol

from rest_framework.request import Request
from django.db.models import Model, QuerySet, Field

from .metadata import FieldMetadata, ModelMetadata
from .literals import AdminAction

class ModelAdminProtocol[TModel: Model](Protocol):
    @property
    def model(self) -> type[TModel]:
        ...

    @property
    def admin_site(self) -> AdminSiteProtocol[TModel]:
        ...

    def __init__(self, model: type[TModel], admin_site: AdminSiteProtocol[TModel]) -> None:
        ...

    def get_queryset(self, request: Request) -> QuerySet[TModel]:
        ...

    def get_list_display(self, request: Request) -> tuple[str, ...]:
        ...

    def get_list_filter(self, request: Request) -> tuple[str, ...]:
        ...

    def get_search_fields(self, request: Request) -> tuple[str, ...]:
        ...

    def get_ordering(self, request: Request) -> tuple[str, ...]:
        ...

    def get_fields(self, request: Request, obj: TModel | None=None) -> tuple[str, ...]:
        ...

    def get_readonly_fields(self, request: Request, obj: TModel | None=None) -> tuple[str, ...]:
        ...

    def has_view_permission(self, request: Request, obj: TModel | None=None) -> bool:
        ...

    def has_add_permission(self, request: Request) -> bool:
        ...

    def has_change_permission(self, request: Request, obj: TModel | None=None) -> bool:
        ...

    def has_delete_permission(self, request: Request, obj: TModel | None=None) -> bool:
        ...


class AdminSiteProtocol[TModel: Model](Protocol):
    @property
    def name(self) -> str:
        ...
    
    def register(self, model: type[TModel], admin_class: type[ModelAdminProtocol[TModel]] | None = None, **options) -> ModelAdminProtocol[TModel]:
        ...

    def unregister(self, model: type[TModel]) -> None:
        ...

    def is_registered(self, model: type[TModel]) -> bool:
        ...

    def get_model_admin(self, model: type[TModel]) -> ModelAdminProtocol[TModel]:
        ...

    def get_registered_models(self) -> tuple[type[TModel], ...]:
        ...

    def get_admins(self) -> tuple[ModelAdminProtocol[TModel], ...]:
        ...


class ModelMetadataBuilderProtocol[TModel: Model](Protocol):
    def build(self, admin: ModelAdminProtocol[TModel], request: Request) -> ModelMetadata:
        ...


class FieldMetadataResolverProtocol[TField: Field](Protocol):
    def can_resolve(self, field: TField) -> bool:
        ...

    def resolve(self, field: TField, *, readonly: bool) -> FieldMetadata:
        ...


class FieldMetadataRegistryProtocol(Protocol):
    def register(self, resolver: FieldMetadataResolverProtocol) -> None:
        ...

    def resolve(self, field: Field, *, readonly: bool) -> FieldMetadata:
        ...


class SerializerProtocol[TModel: Model](Protocol):
    def serialize(self, instance: TModel) -> Mapping[str, Any]:
        ...

    def validate(self, data: Mapping[str, Any], *, instance: TModel | None = None) -> Mapping[str, Any]:
        ...

    def deserialize(self, data: Mapping[str, Any], *, instance: TModel | None = None) -> TModel:
        ...


class QueryBuilderProtocol[TModel: Model](Protocol):
    def build(self, admin: ModelAdminProtocol[TModel], request: Request) -> QuerySet[TModel]:
        ...


class FilterBackendProtocol[TModel: Model](Protocol):
    def filter_queryset(self, request: Request, queryset: QuerySet[TModel], admin: ModelAdminProtocol[TModel]) -> QuerySet[TModel]:
        ...

class SearchBackendProtocol[TModel: Model](Protocol):
    def search(self, request: Request, queryset: QuerySet[TModel], admin: ModelAdminProtocol[TModel]) -> QuerySet[TModel]:
        ...

class OrderingBackendProtocol[TModel: Model](Protocol):
    def order(self, request: Request, queryset: QuerySet[TModel], admin: ModelAdminProtocol[TModel]) -> QuerySet[TModel]:
        ...

@dataclass(frozen=True, slots=True)
class PaginationResult[TModel: Model]:
    items: tuple[TModel, ...]
    total: int
    page: int
    page_size: int
    pages: int

class PaginatorProtocol[TModel: Model](Protocol):
    def paginate(self, queryset: QuerySet[TModel], *, page: int, page_size: int) -> PaginationResult[TModel]:
        ...

class PermissionBackendProtocol[TModel: Model](Protocol):
    def has_permission(self, request: Request, action: AdminAction, obj: TModel | None = None) -> bool:
        ...

@dataclass(frozen=True, slots=True)
class ActionResult:
    success: bool
    message: str | None = None
    affected_count: int = 0

class AdminActionProtocol[TModel: Model](Protocol):
    @property
    def name(self) -> str:
        ...

    @property
    def description(self) -> str:
        ...

    def execute(self, request: Request, queryset: QuerySet[TModel]) -> ActionResult:
        ...

class ActionRegistryProtocol(Protocol):
    def register(self, action: AdminActionProtocol[Model]) -> None:
        ...

    def get_actions(self, admin: ModelAdminProtocol[Model]) -> tuple[AdminActionProtocol[Model], ...]:
        ...

@dataclass(frozen=True, slots=True)
class ModelListResult[TModel: Model]:
    items: tuple[TModel, ...]
    total: int
    page: int
    page_size: int
    pages: int

class ModelServiceProtocol[TModel: Model](Protocol):
    def list(self, request: Request) -> ModelListResult[TModel]:
        ...

    def get(self, request: Request, pk: object) -> TModel:
        ...

    def create(self, request: Request, data: Mapping[str, Any]) -> TModel:
        ...

    def update(self, request: Request, obj: TModel, data: Mapping[str, Any]) -> TModel:
        ...

    def delete(self, request: Request, obj: TModel) -> None:
        ...
