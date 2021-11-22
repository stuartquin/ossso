from rest_framework.request import Request
from rest_framework.response import Response
from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, views, generics
from rest_framework.schemas.openapi import AutoSchema, SchemaGenerator

from api.filters import SAMLConnectionURLFilter
from api.serializers import (
    SAMLConnectionURLSerializer,
    SAMLConnectionSerializer,
    SAMLResponseSerializer,
)
from sso.models import SAMLResponse, SAMLConnection, Domain


class SAMLResponseViewSet(viewsets.ModelViewSet):
    schema = AutoSchema(tags=["response"])
    queryset = SAMLResponse.objects.all().order_by("-created_at")
    serializer_class = SAMLResponseSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "guid"
    lookup_url_kwarg = "code"


class SAMLConnectionViewSet(viewsets.ModelViewSet):
    schema = AutoSchema(tags=["connection"])
    queryset = SAMLConnection.objects.all().order_by("-created_at")
    serializer_class = SAMLConnectionSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "guid"


class SAMLConnectionURLView(generics.RetrieveAPIView):
    schema = AutoSchema(tags=["connection"])
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = SAMLConnectionURLFilter
    serializer_class = SAMLConnectionURLSerializer
    action = "retrieve"

    def retrieve(self, request: Request) -> Response:
        domain = request.GET.get("domain", "")
        # TODO filter by auth
        sso_domain: Domain = get_object_or_404(Domain, domain=domain.strip())
        return Response({"redirect_url": sso_domain.connection.sso_url})


def docs(request: WSGIRequest) -> HttpResponse:
    generator = SchemaGenerator(
        title="OSSSO API Docs",
    )
    return render(request, "api/docs.html", {"schema": generator.get_schema()})
