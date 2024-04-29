from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import TreasuryViewSet, AdminTreasuryViewSet

treasury_list = TreasuryViewSet.as_view({"get": "list"})
treasury_detail = TreasuryViewSet.as_view({"get": "retrieve"})
history = TreasuryViewSet.as_view({"get": "history"})

admin_treasury_list = AdminTreasuryViewSet.as_view({"get": "list", "post": "create"})
admin_treasury_detail = AdminTreasuryViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)
bulk_upload = AdminTreasuryViewSet.as_view({"post": "bulk_upload"})
admin_history = AdminTreasuryViewSet.as_view({"get": "history"})

urlpatterns = format_suffix_patterns(
    [
        path("treasuries/", treasury_list, name="treasury-list"),
        path("treasuries/<int:pk>/", treasury_detail, name="treasury-detail"),
        path("treasuries/<int:pk>/history/", history, name="treasury-history"),
        path("treasuries/admin", admin_treasury_list, name="treasury-admin-list"),
        path(
            "treasuries/admin/<int:pk>/",
            admin_treasury_detail,
            name="treasury-admin-detail",
        ),
        path(
            "treasuries/admin/bulk_upload/",
            bulk_upload,
            name="treasury-admin-bulk-upload",
        ),
        path(
            "treasuries/admin/<int:pk>/history/",
            admin_history,
            name="treasury-admin-history",
        ),
    ]
)
