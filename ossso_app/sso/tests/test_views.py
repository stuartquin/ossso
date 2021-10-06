import json
import httpretty

from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.test import Client
from model_bakery import baker
from unittest.mock import patch

from sso.models import SAMLConnection
from sso.tests.data import CERT, get_saml_response


class SSOSigninTest(TestCase):
    def setUp(self):
        settings.SSO_BASE_URL = "localhost"

    @httpretty.activate(verbose=True, allow_net_connect=False)
    def test_signin(self):
        connection: SAMLConnection = baker.make(
            "sso.SAMLConnection",
            signon_url="https://test.com/abc-123",
            _fill_optional=["cert"],
        )
        httpretty.register_uri(httpretty.GET, r"https://test.com/abc-123.*")

        client = Client()
        response = client.get(
            reverse("sso-signin", args=[connection.guid]), follow=True
        )

        redirect_url, _ = response.redirect_chain[0]
        self.assertRegex(redirect_url, r"https:\/\/test\.com\/abc-123\?SAMLRequest=.*")


class SSOACSTest(TestCase):
    def setUp(self):
        settings.SSO_BASE_URL = "localhost"

    @httpretty.activate(verbose=True, allow_net_connect=False)
    def test_sso_acs(self):
        connection: SAMLConnection = baker.make(
            "sso.SAMLConnection",
            guid="7410c6d0-54f5-4841-af01-279e52f04eb0",
            signon_url="https://login.microsoftonline.com/f0f64571-ea38-4778-908d-0119fcb190f0/saml2",
            idp_entity_id="https://sts.windows.net/f0f64571-ea38-4778-908d-0119fcb190f0/",
            sp_entity_id="localhost/sso/signin/7410c6d0-54f5-4841-af01-279e52f04eb0/",
            provider="azure",
            cert=CERT,
        )

        client = Client()
        with patch("saml2.sigver.SecurityContext.check_signature"):
            response = client.post(
                reverse("sso-acs", args=[connection.guid]),
                {"SAMLResponse": get_saml_response()},
            )

            self.assertEquals(response.status_code, 302)
