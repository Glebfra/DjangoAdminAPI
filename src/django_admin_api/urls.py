from django.urls import path

from . import views

app_name = "admin_api"

urlpatterns = [
    path(
        "models/",
        views.ModelListView.as_view(),
        name="model-list"
    )
]
