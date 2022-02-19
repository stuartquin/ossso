from django.urls import path, include
from web import views

urlpatterns = [
    path("", views.index, name="web_index"),
    path(
        "organization/<str:guid>",
        views.OrganizationDetail.as_view(),
        name="web_organization_detail",
    ),
    path(
        "organization/<str:guid>/edit",
        views.OrganizationEdit.as_view(),
        name="web_organization_edit",
    ),
    path(
        "organization",
        views.OrganizationList.as_view(),
        name="web_organization",
    ),
    path(
        "organization/<str:organization_guid>/connection/<str:guid>/edit",
        views.SAMLConnectionEdit.as_view(),
        name="web_connection_edit",
    ),
    path(
        "organization/<str:organization_guid>/connection/<str:guid>",
        views.SAMLConnectionDetail.as_view(),
        name="web_connection_detail",
    ),
    path(
        "connection/<str:connection_guid>/domain/<str:guid>",
        views.DomainEdit.as_view(),
        name="web_domain_edit",
    ),
    path("accounts/register", views.Register.as_view(), name="web_register"),
    path("accounts/", include("django.contrib.auth.urls")),
]
