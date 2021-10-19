from rest_framework import viewsets
from rest_framework import permissions

from sso.models import SAMLResponse, SAMLConnection
from api.serializers import SAMLConnectionSerializer, SAMLResponseSerializer


class SAMLResponseViewSet(viewsets.ModelViewSet):
    queryset = SAMLResponse.objects.all().order_by("-created_at")
    serializer_class = SAMLResponseSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "guid"
    lookup_url_kwarg = "code"


class SAMLConnectionViewSet(viewsets.ModelViewSet):
    queryset = SAMLConnection.objects.all().order_by("-created_at")
    serializer_class = SAMLConnectionSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "guid"
