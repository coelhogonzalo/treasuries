from rest_framework import serializers
from .models import Treasury
from rest_framework import serializers
from .models import Treasury
from rest_framework.validators import UniqueValidator


class TreasurySerializer(serializers.ModelSerializer):
    company = serializers.CharField(
        max_length=255, validators=[UniqueValidator(queryset=Treasury.objects.all())]
    )
    country = serializers.CharField(max_length=50)
    exchange = serializers.CharField(max_length=50)
    symbol = serializers.CharField(max_length=50)
    filingurl = serializers.URLField(max_length=2000)
    btc = serializers.IntegerField()
    btcc = serializers.CharField(max_length=50)
    btc_source_dt = serializers.DateField()
    tot_balance_sheet = serializers.IntegerField()
    treasury_type = serializers.CharField(max_length=50, default="public")
    dateoffirstbuy = serializers.DateField()
    percentbtc = serializers.CharField(allow_null=True, allow_blank=True, max_length=50)
    info_url = serializers.CharField(allow_null=True, allow_blank=True, max_length=255)
    cssclass = serializers.CharField(allow_null=True, allow_blank=True, max_length=50)

    class Meta:
        model = Treasury
        fields = "__all__"


class UpdateTreasurySerializer(TreasurySerializer):

    class Meta:
        model = Treasury
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False
