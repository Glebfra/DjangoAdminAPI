from dataclasses import asdict
from typing import Any

from django.db.models import Model
from django.views import View
from rest_framework.request import Request
from rest_framework.response import Response

from .registry import AdminSite

class AdminApiView(View):
    """
    Base class for Admin API views.
    """

    site: AdminSite

    def __init__(self, admin_site: AdminSite, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.admin_site = admin_site


class ModelListView(AdminApiView):
    """
    GET /api/admin/models/
    """

    def __init__(self, admin_site: AdminSite, **kwargs: Any) -> None:
        super().__init__(admin_site, **kwargs)

    def get(self, request: Request) -> Response:
        models = tuple(
            self._serialize_model(model)
            for model in self.admin_site.get_registered_models()
        )

        return Response({
            "results": models
        })

    @staticmethod
    def _serialize_model(model: type[Model]) -> dict[str, str]:
        meta = model._meta

        return {
            "app_label": meta.app_label,
            "model_name": str(meta.model_name),
            "verbose_name": str(meta.verbose_name),
            "verbose_name_plural": str(meta.verbose_name_plural)
        }


class ModelMetadataView(AdminApiView):
    """
    GET /api/admin/models/{app_label}/{model_name}/
    """

    def __init__(self, admin_site: AdminSite, **kwargs: Any) -> None:
        super().__init__(admin_site, **kwargs)

    def get(self, request: Request, app_label: str, model_name: str) -> Response:
        model = self._get_model(app_label, model_name)        
        admin = self.admin_site.get_model_admin(model)
        registry = create_default_field_metadata_registry()

        builder = ModelMetadataBuilder(field_registry=registry)
        metadata = builder.build(admin, request)

        return Response(asdict(metadata))

    def _get_model(self, app_label: str, model_name: str):
        for model in self.admin_site.get_registered_models():
            meta = model._meta

            if meta.app_label == app_label and meta.model_name == model_name:
                return model
