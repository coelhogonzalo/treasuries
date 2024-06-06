from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render({}, request))


def countries(request):
    template = loader.get_template("countries.html")
    return HttpResponse(template.render({}, request))


def miners(request):
    template = loader.get_template("miners.html")
    return HttpResponse(template.render({}, request))


def etfs(request):
    template = loader.get_template("etfs.html")
    return HttpResponse(template.render({}, request))


def etf_aum_history(request):
    template = loader.get_template("etf_aum_history.html")
    return HttpResponse(template.render({}, request))


def net_flows(request):
    template = loader.get_template("net_flows.html")
    return HttpResponse(template.render({}, request))
