from rest_framework.generics import get_object_or_404
from api.serializers import OrganizationSerializer
from sso.models import UserProfile, Organization
from django.contrib.auth.models import User
from django.db.models.query import QuerySet


def get_organizations_for_user_profile(
    user_profile: UserProfile,
) -> "QuerySet[Organization]":
    return user_profile.account.organization_set.all()


def create_organization(user: User, data: dict) -> Organization:
    serializer = OrganizationSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save(account=user.userprofile.account)
    return serializer.instance


def update_organization(user: User, guid: str, data: dict) -> Organization:
    account = user.userprofile.account
    organization = get_object_or_404(account.organization_set, guid=guid)

    serializer = OrganizationSerializer(organization, data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer.instance
