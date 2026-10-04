from django.db.models import Model, QuerySet
from rest_framework.request import Request

from .types import AdminSiteProtocol, AdminAction, ModelAdminProtocol

class ModelAdmin[TModel: Model](ModelAdminProtocol[TModel]):
    """
    Configuration and behavior for a single Django model
    exposed through Admin API.
    """

    list_display: tuple[str, ...] = ()
    list_filter: tuple[str, ...] = ()
    search_fields: tuple[str, ...] = ()
    ordering: tuple[str, ...] = ()

    fields: tuple[str, ...] | None = None
    readonly_fields: tuple[str, ...] = ()

    list_per_page: int = 100

    def __init__(self, model: type[TModel], admin_site: AdminSiteProtocol[TModel]) -> None:
        self._model = model
        self._admin_site = admin_site

    @property
    def model(self) -> type[TModel]:
        return self._model

    @property
    def admin_site(self) -> AdminSiteProtocol[TModel]:
        return self._admin_site

    def get_queryset(self, request: Request) -> QuerySet[TModel]:
        return self.model.objects.all()

    def get_list_display(self, request: Request) -> tuple[str, ...]:
        if self.list_display:
            return self.list_display

        assert self.model._meta.pk is not None
        return tuple(self.model._meta.pk.name)

    def get_list_filter(self, request: Request) -> tuple[str, ...]:
        return self.list_filter

    def get_search_fields(self, request: Request) -> tuple[str, ...]:
        return self.search_fields

    def get_ordering(self, request: Request) -> tuple[str, ...]:
        return self.ordering

    def get_fields(self, request: Request, obj: TModel | None = None) -> tuple[str, ...]:
        if self.fields is not None:
            return self.fields

        return tuple(
            field.name
            for field in self.model._meta.fields
            if field.editable
            and field.name not in self.readonly_fields
        )

    def get_readonly_fields(self, request: Request, obj: TModel | None = None) -> tuple[str, ...]:
        return self.readonly_fields

    def has_view_permission(self, request: Request, obj: TModel | None = None) -> bool:
        return request.user.has_perm(self._permission_name(AdminAction.VIEW))

    def has_add_permission(self, request: Request) -> bool:
        return request.user.has_perm(self._permission_name(AdminAction.ADD))

    def has_change_permission(self, request: Request, obj: TModel | None = None) -> bool:
        return request.user.has_perm(self._permission_name(AdminAction.CHANGE))

    def has_delete_permission(self, request: Request, obj: TModel | None = None) -> bool:
        return request.user.has_perm(self._permission_name(AdminAction.DELETE))

    def _permission_name(self, action: str) -> str:
        meta = self.model._meta
        return f"{meta.app_label}.{action}_{meta.model_name}"
