from sso.models import SAMLConnection, SAMLResponse
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
