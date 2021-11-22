import json

from model_bakery import baker
from django.test import TestCase
from django.urls.base import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


from sso.models import Domain


class APIConnectionViewTest(TestCase):
    def test_connections(self):
        self.assertEqual(True, True)


class SAMLConnectionViewTest(TestCase):
    def test_get_redirect_url(self):
        domain: Domain = baker.make(
            "sso.Domain", connection=baker.make("sso.SAMLConnection")
        )
        token = baker.make(Token)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = client.get(
            reverse("api-connection-url") + f"?domain={domain.domain}"
        )

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            json.loads(response.content), {"redirect_url": domain.connection.sso_url}
        )
