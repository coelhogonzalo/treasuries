import factory
from .models import Treasury


class TreasuryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Treasury

    company = factory.Faker("company")
    country = factory.Faker("country")
    symbol = factory.Faker("word")
    exchange = factory.Faker("word")
    filingurl = factory.Faker("url")
    btc = factory.Faker("random_int")
    btc_source_dt = factory.Faker("date")
    type = factory.Faker("word")
    dateoffirstbuy = factory.Faker("date")
    info_url = factory.Faker("url")
    cssclass = factory.Faker("word")
    miner = False