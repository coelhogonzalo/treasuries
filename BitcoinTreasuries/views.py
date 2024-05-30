from django.http import HttpResponse
from django.template import loader

from treasuries.domain import get_bitcoin_price
from treasuries.models import Treasury


def index(request):
    template = loader.get_template("index.html")
    etfs = Treasury.objects.filter(treasury_type="etf")
    context = {
        "etfs": etfs,
        "btc_price": get_bitcoin_price(),
    }
    return HttpResponse(template.render(context, request))
