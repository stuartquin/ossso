from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.schemas.openapi import AutoSchema

from sso.models import SAMLResponse, SAMLConnection
from api.serializers import SAMLConnectionSerializer, SAMLResponseSerializer


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


def docs(request: WSGIRequest) -> HttpResponse:
    return render(request, "api/docs.html")
