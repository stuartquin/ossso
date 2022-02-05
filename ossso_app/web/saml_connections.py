from rest_framework.generics import get_object_or_404
from api.serializers import SAMLConnectionSerializer
from sso.models import SAMLConnection, Organization


def create_saml_connection(
    organization: Organization, data: dict
) -> SAMLConnectionSerializer:
    serializer = SAMLConnectionSerializer(data=data)

    if serializer.is_valid():
        serializer.save(organization=organization)
    return serializer


def update_saml_connection(
    organization: Organization, guid: str, data: dict
) -> SAMLConnectionSerializer:
    connection = get_object_or_404(organization.samlconnection_set, guid=guid)

    serializer = SAMLConnectionSerializer(connection, data=data)
    if serializer.is_valid():
        serializer.save()
    return serializer
