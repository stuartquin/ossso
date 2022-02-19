from django.urls import path, include
from django.contrib.auth.decorators import login_required
from web import views

urlpatterns = [
    path("", login_required(views.OrganizationList.as_view()), name="web_index"),
    path(
        "organization/<str:guid>",
        login_required(views.OrganizationDetail.as_view()),
        name="web_organization_detail",
    ),
    path(
        "organization/<str:guid>/edit",
        login_required(views.OrganizationEdit.as_view()),
        name="web_organization_edit",
    ),
    path(
        "organization",
        login_required(views.OrganizationList.as_view()),
        name="web_organization",
    ),
    path(
        "organization/<str:organization_guid>/connection/<str:guid>/edit",
        login_required(views.SAMLConnectionEdit.as_view()),
        name="web_connection_edit",
    ),
    path(
        "organization/<str:organization_guid>/connection/<str:guid>",
        login_required(views.SAMLConnectionDetail.as_view()),
        name="web_connection_detail",
    ),
    path(
        "connection/<str:connection_guid>/domain/<str:guid>",
        login_required(views.DomainEdit.as_view()),
        name="web_domain_edit",
    ),
    path("accounts/register", views.Register.as_view(), name="web_register"),
    path("accounts/", include("django.contrib.auth.urls")),
]
