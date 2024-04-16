from rest_framework import serializers
from .models import Treasury

class TreasurySerializer(serializers.ModelSerializer):
    class Meta:
        model = Treasury
        fields = '__all__'
