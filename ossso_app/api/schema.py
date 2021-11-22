from typing import Any
from rest_framework.schemas.openapi import AutoSchema


class RedirectSchema(AutoSchema):
    def get_responses(self, path: str, method: str) -> dict[str, Any]:
        return {"302": {"description": "Identity provider sign-in URL"}}
