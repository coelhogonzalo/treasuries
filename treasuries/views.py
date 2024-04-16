from rest_framework import viewsets
from .models import Treasury
from .serializers import TreasurySerializer

class TreasuryViewSet(viewsets.ModelViewSet):
    queryset = Treasury.objects.all()
    serializer_class = TreasurySerializer
