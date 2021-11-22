from sso.models import SAMLConnection
from django_filters import CharFilter, FilterSet


class SAMLConnectionURLFilter(FilterSet):
    domain = CharFilter(required=True, label="Domain for SSO redirection")

    class Meta:
        model = SAMLConnection
        fields = ["domain"]
