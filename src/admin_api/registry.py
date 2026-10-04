from typing import cast

from django.db.models import Model

from admin_api.exceptions import AlreadyRegisteredError, NotRegisteredError
from admin_api.options import ModelAdmin
from admin_api.types import AdminSiteProtocol, ModelAdminProtocol


class AdminSite(AdminSiteProtocol):
    def __init__(self, name: str = "admin") -> None:
        self._name = name

        self._registry: dict[type[Model], ModelAdminProtocol[Model]] = {}

    @property
    def name(self) -> str:
        return self._name

    def register[TModel: Model](self, model: type[TModel], admin_class: type[ModelAdminProtocol[TModel]] | None = None, **options) -> ModelAdminProtocol[TModel]:
        if model in self._registry:
            raise AlreadyRegisteredError(model)

        if admin_class is None:
            admin_class = ModelAdmin

        admin_instance = admin_class(
            model=model,
            admin_site=self
        )

        erased_admin = cast(
            ModelAdminProtocol[Model],
            admin_instance
        )

        self._registry[model] = erased_admin

        return admin_instance

    def unregister(self, model: type[Model]) -> None:
        if model not in self._registry:
            raise NotRegisteredError(model)

        del self._registry[model]

    def is_registered(self, model: type[Model]) -> bool:
        return model in self._registry

    def get_model_admin[TModel: Model](self, model: type[TModel]) -> ModelAdminProtocol[TModel]:
        try:
            admin = self._registry[model]
        except KeyError:
            raise NotRegisteredError(model) from None

        return cast(ModelAdminProtocol[TModel], admin)

    def get_registered_models(self) -> tuple[type[Model], ...]:
        return tuple(self._registry)

    def get_admins(self) -> tuple[ModelAdminProtocol[Model], ...]:
        return tuple(self._registry.values())

    @property
    def urls(self):
        from .urls import get_urls
        return get_urls(self)


site = AdminSite()


def register[TModel: Model](*models: type[TModel], site: AdminSite = site):
    """
    Register one or more Django models.

    Example:

        @admin.register(Page)
        class PageAdmin(admin.ModelAdmin[Page]):
            ...
    """

    def decorator(admin_class: type[ModelAdminProtocol[TModel]]):
        for model in models:
            site.register(model=model, admin_class=admin_class)
        return admin_class
    return decorator
