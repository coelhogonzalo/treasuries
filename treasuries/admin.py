from django.contrib import admin
from .models import TreasuriesAPIKey, Treasury
from rest_framework_api_key.admin import APIKeyModelAdmin
from rest_framework_api_key.models import APIKey

# Register your models here.
class TreasuriesAPIKeyModelAdmin(APIKeyModelAdmin):
    list_display = ['prefix', 'name', 'hit_count', 'data_used', 'last_used', 'created', 'expiry_date', 'has_expired', 'id']
    readonly_fields = ['hit_count', 'data_used', 'last_used']
    def get_readonly_fields(self, request, obj=None):
        return ['prefix', 'hit_count', 'data_used', 'last_used']

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj=obj)
        if obj is None:
            fields_to_hide = ['prefix', 'hit_count', 'data_used', 'last_used']
            for field_to_hide in fields_to_hide:
                fields.remove(field_to_hide)
        return fields
admin.site.unregister(APIKey)
admin.site.register(TreasuriesAPIKey, TreasuriesAPIKeyModelAdmin)
admin.site.register(Treasury)