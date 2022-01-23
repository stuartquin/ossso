from rest_framework.generics import get_object_or_404
from sso.models import Organization
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from api.serializers import OrganizationSerializer
from django.http.request import HttpRequest
from django.shortcuts import redirect, render

from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer

from web.organizations import (
    get_organizations_for_user_profile,
    create_organization,
    update_organization,
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
            create_organization(request.user, request.data)
        else:
            update_organization(request.user, guid, request.data)

        return redirect("web_organization")
