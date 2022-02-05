from rest_framework.generics import get_object_or_404
from api.serializers import DomainSerializer
from sso.models import SAMLConnection, Organization


def create_domain(connection: SAMLConnection, data: dict) -> DomainSerializer:
    serializer = DomainSerializer(data=data)

    if serializer.is_valid():
        serializer.save(connection=connection)
    return serializer


def update_domain(
    connection: SAMLConnection, guid: str, data: dict
) -> DomainSerializer:
    connection = get_object_or_404(connection.domain_set, guid=guid)

    serializer = DomainSerializer(connection, data=data)
    if serializer.is_valid():
        serializer.save()
    return serializer
