from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import TreasuryViewSet


treasury_list = TreasuryViewSet.as_view({"get": "list", "post": "create"})
treasury_detail = TreasuryViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)

urlpatterns = format_suffix_patterns(
    [
        path("treasuries/", treasury_list, name="treasury-list"),
        path("treasuries/<int:pk>/", treasury_detail, name="treasury-detail"),
    ]
)
