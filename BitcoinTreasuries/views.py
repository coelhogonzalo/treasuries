from django.http import HttpResponse
from django.template import loader

from treasuries.models import Treasury


def index(request):
    template = loader.get_template("index.html")
    etfs = Treasury.objects.filter(treasury_type="etf")
    context = {
        "etfs": etfs
    }
    return HttpResponse(template.render(context, request))