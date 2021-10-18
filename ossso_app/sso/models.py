import uuid
from django.db import models
from django.urls import reverse
from django.conf import settings


def get_base_url() -> str:
    return settings.SSO_BASE_URL


class Account(models.Model):
    guid = models.UUIDField(default=uuid.uuid4, db_index=True)


class Organization(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    guid = models.UUIDField(default=uuid.uuid4, db_index=True)
    name = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class SAMLConnection(models.Model):
    guid = models.UUIDField(default=uuid.uuid4, db_index=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    provider = models.CharField(max_length=2048, db_index=True)
    idp_entity_id = models.CharField(max_length=2048)
    sp_entity_id = models.CharField(max_length=2048)
    signon_url = models.CharField(max_length=2048)
    cert = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def acs_url(self):
        return "".join([get_base_url(), reverse("sso-acs", args=[self.guid])])

    @property
    def sso_url(self):
        return "".join([get_base_url(), reverse("sso-signin", args=[self.guid])])

    def __str__(self):
        return f"{self.provider} [{self.organization.id}]"


class SAMLResponse(models.Model):
    guid = models.UUIDField(default=uuid.uuid4, db_index=True)
    connection = models.ForeignKey(SAMLConnection, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    retrieved_at = models.DateTimeField(blank=True, null=True)
    authn_response = models.TextField()
    identity = models.TextField()
    user_name = models.TextField()
