from django.http import HttpResponse
from django.template import loader

from treasuries.domain import get_context


def index(request):
    template = loader.get_template("index.html")
    context = get_context()
    context["base_domain"] = request.get_host()
    return HttpResponse(template.render(context, request))
