from rest_framework.renderers import JSONRenderer
from rest_framework.status import is_success


class Farm360ResponeRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context["response"]

        modified_data = {}
        modified_data["statusCode"] = response.status_code
        modified_data["success"] = is_success(response.status_code)

        if isinstance(data, dict) and data.get("message"):
            modified_data["message"] = data.pop("message")

        if is_success(response.status_code):
            modified_data["data"] = data
        else:
            modified_data["errors"] = data

        return super().render(modified_data, accepted_media_type, renderer_context)
