from django.urls import path
from web import views

urlpatterns = [
    path("", views.index, name="web_index"),
    path(
        "organization/<str:guid>",
        views.OrganizationDetail.as_view(),
        name="web_organization_detail",
    ),
    path(
        "organization",
        views.OrganizationList.as_view(),
        name="web_organization",
    ),
    path(
        "organization/<str:organization_guid>/connection/<str:guid>",
        views.SAMLConnectionDetail.as_view(),
        name="web_connection_detail",
    ),
]
