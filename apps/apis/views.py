from django.views.generic import TemplateView


class ScalarAPIView(TemplateView):
    template_name = "apis/scalar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["schema_url"] = "/api/schema/"
        context["title"] = "Platform API"
        return context
