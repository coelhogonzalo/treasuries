from rest_framework_api_key.permissions import HasAPIKey
from treasuries.models import TreasuriesAPIKey


class HasTreasuriesAPIKey(HasAPIKey):
    model = TreasuriesAPIKey

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        return True
