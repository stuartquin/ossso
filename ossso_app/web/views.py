from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from sso.models import Organization, SAMLConnection
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from api.serializers import OrganizationSerializer, SAMLConnectionSerializer
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


class OrganizationDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    authentication_classes = [SessionAuthentication]
    template_name = "organization/detail.html"

    def get(self, request, guid):
        if guid == "new":
            serializer = OrganizationSerializer()
        else:
            organization = get_object_or_404(Organization, guid=guid)
            serializer = OrganizationSerializer(organization)
        return Response({"serializer": serializer, "guid": guid})

    def post(self, request, guid):
        if guid == "new":
            serializer = create_organization(request.user, request.data)
        else:
            serializer = update_organization(request.user, guid, request.data)

        if not serializer.is_valid():
            return Response({"serializer": serializer, "guid": guid})

        return redirect("web_organization")


class SAMLConnectionDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    authentication_classes = [SessionAuthentication]
    template_name = "saml_connection/detail.html"

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
