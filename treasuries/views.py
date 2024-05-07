from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework import viewsets
from rest_framework import filters

import json

from .models import Treasury
from .domain import parse_date

from .serializers import (
    TreasurySerializer,
    UpdateTreasurySerializer,
    HistoryTreasurySerializer,
)


class BaseViewSet(viewsets.ModelViewSet):
    queryset = Treasury.objects.all()
    serializer_class = TreasurySerializer

    @action(detail=True, methods=["get"])
    def history(self, request, pk=None):
        start_date = parse_date(request.query_params.get("start"))
        end_date = parse_date(request.query_params.get("end"))
        treasury = self.get_object()
        history_queryset = treasury.history.all()
        if start_date == "Invalid date format":
            return Response(
                {"error": "Start date is invalid"}, status=status.HTTP_400_BAD_REQUEST
            )
        if end_date == "Invalid date format":
            return Response(
                {"error": "End date is invalid"}, status=status.HTTP_400_BAD_REQUEST
            )
        if start_date:
            history_queryset = history_queryset.filter(history_date__gte=start_date)
        if end_date:
            history_queryset = history_queryset.filter(history_date__lte=end_date)
        serializer = HistoryTreasurySerializer(history_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdminTreasuryViewSet(BaseViewSet):
    queryset = Treasury.objects.all()
    serializer_class = TreasurySerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=["post"])
    def bulk_upload(self, request, *args, **kwargs):
        data = request.data
        if not isinstance(data, list):
            return Response(
                {"error": "Invalid JSON format: expected list of treasuries"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not data:
            return Response(
                {"error": "No data provided"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            new_treasuries = []
            modified_treasuries = []
            for item in data:
                treasury_id = item.get("id")
                treasury = Treasury.objects.filter(id=treasury_id).first()
                if treasury:
                    serializer = UpdateTreasurySerializer(treasury, data=item)
                    if serializer.is_valid(raise_exception=True):
                        serializer.save(partial=True)
                        modified_treasuries.append(serializer.data)
                elif treasury_id:
                    return Response(
                        {"error": "id should not be specified for new treasuries"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:
                    serializer = self.get_serializer(data=item)
                    if serializer.is_valid(raise_exception=True):
                        self.perform_create(serializer)
                        new_treasuries.append(serializer.data)
            headers = self.get_success_headers(serializer.data)
            response_data = {
                "new_treasuries": new_treasuries,
                "modified_treasuries": modified_treasuries,
            }
            return Response(response_data, status=status.HTTP_200_OK, headers=headers)
        except json.JSONDecodeError:
            return Response(
                {"error": "Invalid JSON format"}, status=status.HTTP_400_BAD_REQUEST
            )


class TreasuryViewSet(BaseViewSet):
    permission_classes = [HasAPIKey]
    filter_backends = [filters.SearchFilter]
    search_fields = ['company', 'symbol']

    def get_allowed_methods(self):
        return ["GET"]

    @action(detail=True, methods=["get"])
    def history(self, request, pk=None):
        start_date = parse_date(request.query_params.get("start"))
        end_date = parse_date(request.query_params.get("end"))
        treasury = self.get_object()
        history_queryset = treasury.history.all()
        if start_date == "Invalid date format":
            return Response(
                {"error": "Start date is invalid"}, status=status.HTTP_400_BAD_REQUEST
            )
        if end_date == "Invalid date format":
            return Response(
                {"error": "End date is invalid"}, status=status.HTTP_400_BAD_REQUEST
            )
        if start_date:
            history_queryset = history_queryset.filter(history_date__gte=start_date)
        if end_date:
            history_queryset = history_queryset.filter(history_date__lte=end_date)
        serializer = HistoryTreasurySerializer(history_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
