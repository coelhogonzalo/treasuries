from django.db import models
from simple_history.models import HistoricalRecords
from rest_framework_api_key.models import AbstractAPIKey

from BitcoinTreasuries.constants import BTC_21M_CAP


class Treasury(models.Model):
    company = models.CharField(max_length=255, unique=True)
    country = models.CharField(null=True, blank=True, max_length=50)
    exchange = models.CharField(null=True, blank=True, max_length=50)
    symbol = models.CharField(null=True, blank=True, max_length=50)
    filingurl = models.URLField(null=True, blank=True, max_length=2000)
    btc = models.FloatField()
    btc_source_dt = models.DateField()
    treasury_type = models.CharField(max_length=50, default="public")
    dateoffirstbuy = models.DateField(null=True, blank=True)
    info_url = models.CharField(null=True, blank=True, max_length=255)
    cssclass = models.CharField(null=True, blank=True, max_length=50)
    miner = models.BooleanField(default=False)
    etfshortname = models.CharField(null=True, blank=True, max_length=50)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.id}-{self.company}({self.exchange}:{self.symbol})"

    class Meta:
        verbose_name = "Treasury"
        verbose_name_plural = "Treasuries"

    @property
    def percentage_from_21m(self):
        return round(self.btc * 100 / BTC_21M_CAP, 3)

    @property
    def btc_rounded(self):
        if (self.btc).is_integer():
            return int(self.btc)
        return round(self.btc, 1)

    @property
    def btc_rounded_str(self):
        if (self.btc).is_integer():
            return "{:,.0f}".format(self.btc)
        return "{:,.1f}".format(self.btc)


class TreasuriesAPIKey(AbstractAPIKey):
    hit_count = models.IntegerField(
        default=0, help_text="Number of times this API key has been used."
    )
    data_used = models.FloatField(
        default=0, help_text="Amount of data used (in megabytes)."
    )
    last_used = models.DateField(
        null=True, default=None, help_text="Date when this API key was last used."
    )

    def __str__(self) -> str:
        return f"{self.name}:{self.prefix}"
