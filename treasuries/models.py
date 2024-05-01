from django.db import models
from simple_history.models import HistoricalRecords

class Treasury(models.Model):
    company = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=50)
    exchange = models.CharField(max_length=50)
    symbol = models.CharField(max_length=50)
    filingurl = models.URLField(max_length=2000)
    btc = models.IntegerField()
    btcc = models.CharField(max_length=50)
    btc_source_dt = models.DateField()
    tot_balance_sheet = models.BigIntegerField()
    treasury_type = models.CharField(max_length=50, default="public")
    dateoffirstbuy = models.DateField()
    percentbtc = models.CharField(null=True, blank=True, max_length=50)
    info_url = models.CharField(null=True, blank=True, max_length=255)
    cssclass = models.CharField(null=True, blank=True, max_length=50)
    history = HistoricalRecords()


    def __str__(self):
        return f"{self.id}-{self.company}({self.exchange}:{self.symbol})"
    
    class Meta:
        unique_together = ('exchange', 'symbol',)
        verbose_name = 'Treasuries'
        verbose_name_plural = 'Treasuries'
