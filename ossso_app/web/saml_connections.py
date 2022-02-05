from rest_framework.generics import get_object_or_404
from api.serializers import SAMLConnectionSerializer
from sso.models import SAMLConnection, Organization


def create_saml_connection(organization: Organization, data: dict) -> SAMLConnection:
    serializer = SAMLConnectionSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save(organization=organization)
    return serializer.instance


def update_saml_connection(
    organization: Organization, guid: str, data: dict
) -> SAMLConnection:
    connection = get_object_or_404(organization.samlconnection_set, guid=guid)

    serializer = SAMLConnectionSerializer(connection, data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer.instance
