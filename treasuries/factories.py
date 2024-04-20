import factory
from .models import Treasury

class TreasuryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Treasury

    company = factory.Faker('company')
    country = factory.Faker('country')
    symbol = factory.Faker('word')
    exchange = factory.Faker('word')
    filingurl = factory.Faker('url')
    btc = factory.Faker('random_int')
    btcc = factory.Faker('word')
    btc_source_dt = factory.Faker('date')
    tot_balance_sheet = factory.Faker('random_int')
    treasury_type = factory.Faker('word')
    dateoffirstbuy = factory.Faker('date')
    percentbtc = factory.Faker('word')
    info_url = factory.Faker('url')
    cssclass = factory.Faker('word')