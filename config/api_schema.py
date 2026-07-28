from drf_spectacular.generators import SchemaGenerator
from drf_spectacular.views import SpectacularAPIView


class DynamicSchemaGenerator(SchemaGenerator):
    def get_schema(self, request=None, *, public=False):
        schema = super().get_schema(request=request, public=public)

        if request:
            schema["servers"] = [
                {
                    "url": f"{request.scheme}://{request.get_host()}",
                    "description": "Current environment",
                },
            ]

        return schema


class DynamicSpectacularAPIView(SpectacularAPIView):
    generator_class = DynamicSchemaGenerator
