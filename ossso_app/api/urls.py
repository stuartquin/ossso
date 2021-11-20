from django.urls import path
from rest_framework.schemas import get_schema_view
from rest_framework.routers import SimpleRouter
from api import views


router = SimpleRouter()
router.register(r"v1/response", views.SAMLResponseViewSet, basename="sso")
router.register(r"v1/connection", views.SAMLConnectionViewSet, basename="sso")


urlpatterns = [
    # ...
    # Use the `get_schema_view()` helper to add a `SchemaView` to project URLs.
    #   * `title` and `description` parameters are passed to `SchemaGenerator`.
    #   * Provide view name for use with `reverse()`.
    path(
        "openapi",
        get_schema_view(
            title="OpenSource SSO", description="API for SSO login", version="1.0.0"
        ),
        name="openapi-schema",
    ),
    path("docs", views.docs, name="api-docs"),
] + router.urls
