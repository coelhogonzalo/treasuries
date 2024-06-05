from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render({}, request))


def countries(request):
    template = loader.get_template("countries.html")
    return HttpResponse(template.render({}, request))
