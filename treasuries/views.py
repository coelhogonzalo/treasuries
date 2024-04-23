import json
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from .models import Treasury
from .serializers import TreasurySerializer, UpdateTreasurySerializer
from rest_framework.decorators import action


class TreasuryViewSet(viewsets.ModelViewSet):
    queryset = Treasury.objects.all()
    serializer_class = TreasurySerializer

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
