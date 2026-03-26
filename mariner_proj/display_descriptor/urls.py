from django.urls import path
from . import views

app_name = "display_descriptor"

urlpatterns = [
    path(
        "preview/", views.preview_display_descriptor, name="preview_display_descriptor"
    ),
    path(
        "admin-test/", views.test_config_for_resource, name="test_config_for_resource"
    ),
    path(
        "<str:resource_id>/",
        views.get_display_descriptor,
        name="get_display_descriptor",
    ),
]
