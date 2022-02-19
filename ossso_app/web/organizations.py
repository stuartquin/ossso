from rest_framework.generics import get_object_or_404
from api.serializers import OrganizationSerializer
from sso.models import UserProfile, Organization
from django.contrib.auth.models import User
from django.db.models.query import QuerySet


def get_organizations_for_user_profile(
    user_profile: UserProfile,
) -> "QuerySet[Organization]":
    return user_profile.account.organization_set.prefetch_related(
        "samlconnection_set"
    ).all()


def create_organization(user: User, data: dict) -> OrganizationSerializer:
    serializer = OrganizationSerializer(data=data)
    if serializer.is_valid():
        serializer.save(account=user.userprofile.account)
    return serializer


def update_organization(user: User, guid: str, data: dict) -> OrganizationSerializer:
    account = user.userprofile.account
    organization = get_object_or_404(account.organization_set, guid=guid)

    serializer = OrganizationSerializer(organization, data=data)
    if serializer.is_valid():
        serializer.save()
    return serializer
