from django.contrib.auth import login
from web.accounts import create_user_profile
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.forms import UserCreationForm
from web.domains import create_domain, update_domain
from rest_framework.generics import get_object_or_404
from sso.models import Account, Organization, SAMLConnection
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from api.serializers import (
    DomainSerializer,
    OrganizationSerializer,
    SAMLConnectionSerializer,
)
from django.http.request import HttpRequest
from django.shortcuts import redirect, render

from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer

from web.organizations import (
    get_organizations_for_user_profile,
    create_organization,
    update_organization,
)
from web.saml_connections import (
    create_saml_connection,
    update_saml_connection,
)


def index(request: HttpRequest):
    user = request.user
    return render(request, "index.html")


class Register(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "registration/register.html"

    def get(self, request: HttpRequest):
        form = UserCreationForm()
        return Response({"form": form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            create_user_profile(user, Account.objects.create())
            login(request, user)
            return redirect("web_organization")

        return Response({"form": form})


class OrganizationList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "organization/list.html"

    def get(self, request: HttpRequest):
        return Response(
            {
                "organizations": get_organizations_for_user_profile(
                    request.user.userprofile
                )
            }
        )


class OrganizationEdit(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    template_name = "organization/edit.html"

    def get(self, request, guid):
        is_new = guid == "new"
        if is_new:
            serializer = OrganizationSerializer()
        else:
            organization = get_object_or_404(Organization, guid=guid)
            serializer = OrganizationSerializer(organization)
        return Response({"serializer": serializer, "guid": guid, "is_new": is_new})

    def post(self, request, guid):
        if guid == "new":
            serializer = create_organization(request.user, request.data)
        else:
            serializer = update_organization(request.user, guid, request.data)

        if not serializer.is_valid():
            return Response({"serializer": serializer, "guid": guid})

        return redirect("web_organization")


class OrganizationDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    template_name = "organization/detail.html"

    def get(self, request, guid):
        organization = get_object_or_404(Organization, guid=guid)
        serializer = OrganizationSerializer(organization)
        return Response(
            {
                "serializer": serializer,
                "guid": guid,
                "organization": organization,
            }
        )


class SAMLConnectionEdit(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    template_name = "saml_connection/edit.html"

    def get(self, request, organization_guid, guid):
        user_profile = request.user.userprofile
        organization = get_object_or_404(
            user_profile.account.organization_set, guid=organization_guid
        )
        if guid == "new":
            serializer = SAMLConnectionSerializer()
        else:
            connection = get_object_or_404(organization.samlconnection_set, guid=guid)
            serializer = SAMLConnectionSerializer(connection)
        return Response(
            {
                "serializer": serializer,
                "guid": guid,
                "organization_guid": organization.guid,
            }
        )

    def post(self, request, organization_guid, guid):
        user_profile = request.user.userprofile
        organization = get_object_or_404(
            user_profile.account.organization_set, guid=organization_guid
        )

        if guid == "new":
            serializer = create_saml_connection(organization, request.data)
        else:
            serializer = update_saml_connection(organization, guid, request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "serializer": serializer,
                    "guid": guid,
                    "organization_guid": organization.guid,
                }
            )

        return redirect(
            "web_connection_detail",
            organization_guid=organization.guid,
            guid=serializer.instance.guid,
        )


class SAMLConnectionDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    template_name = "saml_connection/detail.html"

    def get(self, request, organization_guid, guid):
        user_profile = request.user.userprofile
        organization = get_object_or_404(
            user_profile.account.organization_set, guid=organization_guid
        )
        connection = get_object_or_404(organization.samlconnection_set, guid=guid)
        serializer = SAMLConnectionSerializer(connection)
        return Response(
            {
                "serializer": serializer,
                "guid": guid,
                "organization_guid": organization.guid,
            }
        )


class DomainEdit(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    template_name = "domain/edit.html"

    def get(self, request, connection_guid, guid):
        user_profile = request.user.userprofile
        connection = get_object_or_404(
            SAMLConnection.objects.filter(
                organization__in=user_profile.account.organization_set.all()
            ),
            guid=connection_guid,
        )
        if guid == "new":
            serializer = DomainSerializer()
        else:
            domain = get_object_or_404(connection.domain_set, guid=guid)
            serializer = DomainSerializer(domain)

        return Response(
            {
                "serializer": serializer,
                "guid": guid,
                "organization": connection.organization,
                "connection": connection,
            }
        )

    def post(self, request, connection_guid, guid):
        user_profile = request.user.userprofile
        connection = get_object_or_404(
            SAMLConnection.objects.filter(
                organization__in=user_profile.account.organization_set.all()
            ),
            guid=connection_guid,
        )

        if guid == "new":
            serializer = create_domain(connection, request.data)
        else:
            serializer = update_domain(connection, guid, request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "serializer": serializer,
                    "guid": guid,
                    "connection_guid": connection.guid,
                }
            )

        return redirect(
            "web_connection_detail",
            organization_guid=connection.organization.guid,
            guid=connection.guid,
        )
