from rest_framework import serializers
from .models import Treasury
from rest_framework.validators import UniqueValidator
from dateutil import parser


class CustomDateFormatField(serializers.DateField):
    """
    Custom Date Field to parse dates in multiple formats.
    """

    def to_internal_value(self, value):
        try:
            parsed_date = parser.parse(value)
            return parsed_date.date()
        except ValueError:
            try:
                return super().to_internal_value(value)
            except serializers.ValidationError:
                raise serializers.ValidationError(
                    f"Invalid date format for {self.field_name}. Please provide a date in the format 'Month Day, Year' (e.g., 'July 20, 2022') or 'YYYY-MM-DD'."
                )


class TreasurySerializer(serializers.ModelSerializer):
    company = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=Treasury.objects.all())])
    country = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=50)
    exchange = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=50)
    symbol = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=50)
    filingurl = serializers.URLField(required=False, allow_null=True, allow_blank=True, max_length=2000)
    btc = serializers.FloatField()
    btc_source_dt = CustomDateFormatField()
    treasury_type = serializers.CharField(max_length=50, default="public")
    dateoffirstbuy = CustomDateFormatField(required=False, allow_null=True)
    info_url = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=255)
    cssclass = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=50)
    etfshortname = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=50)
    miner = serializers.BooleanField(required=False)

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


class HistoryTreasurySerializer(TreasurySerializer):
    history_date = serializers.DateTimeField(read_only=True)
