import os
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.http import require_GET

from treasuries.domain import get_treasury_by_info_url


def index(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render({}, request))


def countries(request):
    template = loader.get_template("countries.html")
    return HttpResponse(template.render({}, request))


def miners(request):
    template = loader.get_template("miners.html")
    return HttpResponse(template.render({}, request))


def usetfs(request):
    template = loader.get_template("usetfs.html")
    return HttpResponse(template.render({}, request))


def etf_aum_history(request):
    template = loader.get_template("etf_aum_history.html")
    return HttpResponse(template.render({}, request))


def net_flows(request):
    template = loader.get_template("net_flows.html")
    return HttpResponse(template.render({}, request))


def detail_view(request, info_url):
    treasury = get_treasury_by_info_url(info_url=info_url)
    treasury.info_url = None  # This is done to reuse treasury_row.html
    template_path = f"entities/{info_url}.html"
    if not os.path.exists(f"treasuries/templates/{template_path}"):
        template_path = "components/detail.html"
    template = loader.get_template(template_path)
    return HttpResponse(template.render({"treasury": treasury}, request))


@require_GET
def robots_txt(request):
    return HttpResponse(robots_txt_content, content_type="text/plain")


robots_txt_content = """\
User-Agent: *
Disallow: /private/
Disallow: /junk/

User-agent: GPTBot
Disallow: /
"""
