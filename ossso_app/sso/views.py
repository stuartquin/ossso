import logging
from functools import lru_cache

from saml2 import BINDING_HTTP_POST, BINDING_HTTP_REDIRECT, entity, SAMLError

from saml2.client import Saml2Client
from saml2.config import Config as Saml2Config

from django.contrib.auth import login, load_backend
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.core.handlers.wsgi import WSGIRequest
from django.core.exceptions import PermissionDenied

from sso.models import SAMLConnection

logger = logging.getLogger(__name__)


def get_metadata_xml(saml_connection: SAMLConnection) -> str:
    cert = saml_connection.cert
    entity_id = saml_connection.idp_entity_id
    signon_url = saml_connection.signon_url
    xml_str = f"""
<EntityDescriptor entityID="{entity_id}" xmlns="urn:oasis:names:tc:SAML:2.0:metadata">
  <IDPSSODescriptor protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol">
    <KeyDescriptor use="signing">
      <KeyInfo xmlns="http://www.w3.org/2000/09/xmldsig#">
          <X509Data>
          <X509Certificate>{cert}</X509Certificate>
          </X509Data>
      </KeyInfo>
    </KeyDescriptor>
    <SingleSignOnService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect" Location="{signon_url}" />
  </IDPSSODescriptor>
</EntityDescriptor>
    """
    return xml_str


def get_saml_connection(guid: str) -> SAMLConnection:
    return SAMLConnection.objects.get(guid=guid)


@lru_cache()
def get_saml_client_config(guid: str) -> Saml2Config:
    saml_connection = get_saml_connection(guid)
    acs_url = saml_connection.acs_url
    metadata = {"inline": [get_metadata_xml(saml_connection)]}

    service_sp_data = {
        "endpoints": {
            "assertion_consumer_service": [
                (acs_url, BINDING_HTTP_REDIRECT),
                (acs_url, BINDING_HTTP_POST),
            ],
        },
        "allow_unsolicited": True,
        "authn_requests_signed": False,
        "logout_requests_signed": True,
        "want_assertions_signed": True,
        "want_response_signed": False,
    }

    saml_settings = {
        "metadata": metadata,
        "service": {"sp": service_sp_data},
    }

    saml_settings["entityid"] = saml_connection.sp_entity_id

    sp_config = Saml2Config()
    sp_config.load(saml_settings)
    sp_config.allow_unknown_attributes = True

    return sp_config


def get_saml_client(guid: str) -> Saml2Client:
    return Saml2Client(config=get_saml_client_config(guid))


@csrf_exempt
def sso_acs(request: WSGIRequest, guid: str) -> HttpResponseRedirect:
    """
    This endpoint is invoked by the SSO SAML system, for example Okta, when the User
    attempts to login via that SSO system.
    """

    try:

        saml_client = get_saml_client(guid)
        resp = request.POST.get("SAMLResponse", None)
        if not resp:
            errmsg = "SAML2: missing response"
            logger.error(errmsg)
            raise PermissionDenied(errmsg)

        authn_response = saml_client.parse_authn_request_response(
            xmlstr=resp, binding=entity.BINDING_HTTP_POST
        )

        if authn_response is None:
            errmsg = "SAML2: failed to parse response"
            logger.error(errmsg)
            raise PermissionDenied(errmsg)

    except SAMLError as exc:
        errmsg = f"SAML2 error: {str(exc)}"
        logger.error(errmsg)
        raise PermissionDenied(errmsg)

    user_name = authn_response.name_id.text
    backend_name = "django.contrib.auth.backends.RemoteUserBackend"
    backend_obj = load_backend(backend_name)

    # the call to authenticate will call the configure_user method if it
    # exists; the backend is responsible for implementing the necessary
    # configuration options.

    request.META["SAML2_AUTH_RESPONSE"] = authn_response
    user_obj = backend_obj.authenticate(request, user_name)

    logger.info("get_identity")
    logger.info(authn_response.get_identity())
    if not user_obj:
        errmsg = f"SAML2: no-authenticate user {user_name}"
        logger.error(errmsg)
        raise PermissionDenied(errmsg)

    # Login user and redirect to the "next URL"

    user_obj.backend = backend_name
    login(request, user_obj)
    return HttpResponseRedirect("https://example.com?code=abc-123")


def signin(request: WSGIRequest, guid: str) -> HttpResponseRedirect:
    """
    This route is invoked when the User attempts to login to the application
    without first going through the SSO SAML system.  As a result of executing
    this function the User's browswer should be redirected to the SSO system.
    """

    # Next we need to obtain the SSO system URL to direct the User's browser to
    # that system so that they can perform the login.  We use the RelayState
    # URL parameter to pass the 'next-url' value back to the sso handler.

    saml_client = get_saml_client(guid)
    req_id, info = saml_client.prepare_for_authenticate()

    redirect_url = dict(info["headers"])["Location"]

    # This causes the web client to go to the SSO SAML system to force the use
    # to use that system to authenticate.

    return HttpResponseRedirect(redirect_url)
