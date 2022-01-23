from sso.models import Account, Organization, SAMLConnection, SAMLResponse
from rest_framework import serializers


class SAMLResponseSerializer(serializers.ModelSerializer):
    identity = serializers.JSONField(source="identity_json", read_only=True)

    class Meta:
        model = SAMLResponse
        fields = ["guid", "identity", "user_name", "connection"]


class SAMLConnectionSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SAMLConnection
        fields = [
            "guid",
            "organization",
            "provider",
            "idp_entity_id",
            "sp_entity_id",
            "signon_url",
            "cert",
            "created_at",
        ]


class SAMLConnectionURLSerializer(serializers.Serializer):
    redirect_url = serializers.CharField(
        read_only=True, help_text="URL to redirect to Identity Provider sign-in page"
    )


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["guid"]


class OrganizationSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    account = AccountSerializer(read_only=True)
    guid = serializers.CharField(read_only=True)

    class Meta:
        model = Organization
        fields = ["guid", "name", "created_at", "redirect_uri", "account"]
