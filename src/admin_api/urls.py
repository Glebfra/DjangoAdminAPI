from django.urls import path

from .views import ModelListView, ModelMetadataView


app_name = "admin_api"


def get_urls(admin_site):
    return (
        [
            path("models/", ModelListView.as_view(admin_site=admin_site), name="model-list"),
            path("models/<str:app_label>/<str:model_name>/", ModelMetadataView.as_view(admin_site=admin_site), name="model-metadata"),
        ],
        app_name,
        app_name,
    )
