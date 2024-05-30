from datetime import datetime
from .models import TreasuriesAPIKey
from rest_framework_api_key.crypto import KeyGenerator
import sys
import logging

logging.basicConfig(level=logging.INFO)


class DataUsageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        api_key = self.get_api_key(request)

        response = self.get_response(request)

        if api_key:
            data_used = sys.getsizeof(response.content) / (
                1024 * 1024
            )  # 1 MB = 1024 * 1024 bytes
            api_key.data_used += data_used
            api_key.hit_count += 1
            api_key.last_used = datetime.now()
            logging.info(
                f"API key {api_key.name}:{api_key.prefix} made a {request.method} request to {request.path} with a {data_used} MB response"
            )
            api_key.save()

        return response

    def get_api_key(self, request):
        api_key_header = request.headers.get("Authorization")
        if api_key_header and api_key_header.startswith("Api-Key "):
            api_key_value = api_key_header.split(" ")[1]
            try:
                hashed_value = KeyGenerator().hash(api_key_value)
                api_key = TreasuriesAPIKey.objects.get(hashed_key=hashed_value)
                return api_key
            except TreasuriesAPIKey.DoesNotExist:
                pass
        return None
