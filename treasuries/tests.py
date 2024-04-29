import datetime
from django.utils import timezone
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch, Mock
from rest_framework_api_key.models import APIKey
from django.contrib.auth.models import User
from django.db.models import Max

from treasuries.models import Treasury
from treasuries.serializers import TreasurySerializer
from treasuries.factories import TreasuryFactory
from treasuries.domain import parse_date
from faker import Faker

def getAdminClient():
    fake = Faker()
    username = fake.pystr(min_chars=12, max_chars=12)
    password = fake.pystr(min_chars=12, max_chars=12)
    client = APIClient()
    my_admin = User.objects.create_superuser(username, f"{username}@test.com", password)
    client.login(username=my_admin.username, password=password)
    return client

class TreasuriesTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        _, key = APIKey.objects.create_key(name="test")
        authorization = f"Api-Key {key}"
        cls.client = APIClient()
        cls.client.credentials(HTTP_AUTHORIZATION=authorization)
        password = "mypassword"
        my_admin = User.objects.create_superuser("myuser", "myemail@test.com", password)
        cls.client.login(username=my_admin.username, password=password)
        cls.treasury = {
            "company": "Tesla, IncTEST",
            "country": "US",
            "symbol": "TSLATEST",
            "exchange": "NADQTEST",
            "percentbtc": None,
            "info_url": "/tesla/",
            "filingurl": "https://tesla.com",
            "btc": 9720,
            "btcc": "9,720",
            "btc_source_dt": "2020-04-02",
            "tot_balance_sheet": 68513000000,
            "treasury_type": "public",
            "dateoffirstbuy": "2020-04-02",
            "cssclass": "tesla-treasuries",
        }
# Permissions tests
    def test_get_treasuries_API_key_missing(self):
        url = reverse("treasury-list")
        response = APIClient().get(url)

        treasuries = Treasury.objects.all()
        TreasurySerializer(treasuries, many=True)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_post_treasury_not_admin_authorization(self):
        url = reverse("treasury-admin-list")
        response = APIClient().post(
            url, TreasuriesTestCase.treasury, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# Domain tests
    def test_to_string(self):
        treasury = TreasuryFactory.create()
        self.assertEqual(
            str(treasury),
            f"{treasury.id}-{treasury.company}({treasury.exchange}:{treasury.symbol})",
        )
        
    def test_parse_date_valid_date(self):
        date_str = "20220202"
        expected_result = datetime.datetime(2022, 2, 2)
        result = parse_date(date_str)
        self.assertEqual(result, expected_result)

    def test_parse_date_valid_date_year(self):
        date_str = "2022"
        expected_result = datetime.datetime(2022, 1, 1)
        result = parse_date(date_str)
        self.assertEqual(result, expected_result)

    def test_parse_date_valid_date_year_month(self):
        date_str = "202204"
        expected_result = datetime.datetime(2022, 4, 1)
        result = parse_date(date_str)
        self.assertEqual(result, expected_result)

    def test_parse_date_valid_datetime(self):
        date_str = "20220202040530"
        expected_result = datetime.datetime(2022, 2, 2, 4, 5, 30)
        result = parse_date(date_str)
        self.assertEqual(result, expected_result)

    def test_parse_date_valid_datetime_hours(self):
        date_str = "2022020204"
        expected_result = datetime.datetime(2022, 2, 2, 4)
        result = parse_date(date_str)
        self.assertEqual(result, expected_result)

    def test_parse_date_valid_datetime_hours_minutes(self):
        date_str = "202202020435"
        expected_result = datetime.datetime(2022, 2, 2, 4, 35)
        result = parse_date(date_str)
        self.assertEqual(result, expected_result)

    def test_parse_date_invalid_date_format(self):
        date_str = "20220101fd"
        self.assertEqual(parse_date(date_str), "Invalid date format")

    def test_parse_date_empty_string(self):
        date_str = ""
        self.assertEqual(parse_date(date_str), None)

# Admin tests
    def test_post_treasury(self):
        password = "mypassword3"
        my_admin = User.objects.create_superuser("myuser3", "myemail3@test.com", password)
        client = getAdminClient()
        client.login(username=my_admin.username, password=password)
        url = reverse("treasury-admin-list")
        response = client.post(
            url, TreasuriesTestCase.treasury, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["company"], TreasuriesTestCase.treasury["company"]
        )
        self.assertEqual(
            response.data["country"], TreasuriesTestCase.treasury["country"]
        )
        self.assertEqual(response.data["symbol"], TreasuriesTestCase.treasury["symbol"])
        self.assertEqual(
            response.data["exchange"], TreasuriesTestCase.treasury["exchange"]
        )
        self.assertEqual(
            response.data["filingurl"], TreasuriesTestCase.treasury["filingurl"]
        )
        self.assertEqual(response.data["btc"], TreasuriesTestCase.treasury["btc"])
        self.assertEqual(response.data["btcc"], TreasuriesTestCase.treasury["btcc"])
        self.assertEqual(
            response.data["btc_source_dt"], TreasuriesTestCase.treasury["btc_source_dt"]
        )
        self.assertEqual(
            response.data["tot_balance_sheet"],
            TreasuriesTestCase.treasury["tot_balance_sheet"],
        )
        self.assertEqual(
            response.data["treasury_type"], TreasuriesTestCase.treasury["treasury_type"]
        )
        self.assertEqual(
            response.data["dateoffirstbuy"],
            TreasuriesTestCase.treasury["dateoffirstbuy"],
        )
        self.assertEqual(
            response.data["percentbtc"], TreasuriesTestCase.treasury["percentbtc"]
        )
        self.assertEqual(
            response.data["info_url"], TreasuriesTestCase.treasury["info_url"]
        )
        self.assertEqual(
            response.data["cssclass"], TreasuriesTestCase.treasury["cssclass"]
        )

    def test_patch_treasury(self):
        treasury = TreasuryFactory.create()
        url = reverse("treasury-admin-detail", kwargs={"pk": treasury.pk})
        client = getAdminClient()
        response = client.get(url)
        old_exchange = response.data["exchange"]

        data = {"exchange": "NEW-EXCHANGE"}
        response = client.patch(url, data, format="json")
        treasury = Treasury.objects.get(pk=treasury.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data["exchange"], old_exchange)
        self.assertEqual(response.data["exchange"], treasury.exchange)

    def test_delete_treasury(self):
        treasury = TreasuryFactory.create()
        url = reverse("treasury-admin-detail", kwargs={"pk": treasury.pk})
        response = TreasuriesTestCase.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Treasury.objects.filter(pk=treasury.pk).count(), 0)

    def test_admin_bulk_upload(self):
        url = reverse("treasury-admin-bulk-upload")
        treasury_data = [
            {
                "company": "MicroStrategyTEST",
                "country": "US",
                "symbol": "MSTRTEST",
                "exchange": "NADQTEST",
                "percentbtc": None,
                "filingurl": "https://microstrategies.com",
                "info_url": "/microstrategy/",
                "btc": 214746,
                "btcc": "214,246",
                "btc_source_dt": "2020-04-02",
                "tot_balance_sheet": 2443079000,
                "treasury_type": "public",
                "dateoffirstbuy": "2020-04-02",
                "cssclass": "microstategies-treasuries",
            },
            TreasuriesTestCase.treasury,
        ]
        response = TreasuriesTestCase.client.post(url, treasury_data, format="json")
        new_treasury = response.data["new_treasuries"][0]
        for key, value in treasury_data[0].items():
            self.assertEqual(new_treasury[key], value)
        new_treasury = response.data["new_treasuries"][1]
        for key, value in treasury_data[1].items():
            self.assertEqual(new_treasury[key], value)

    def test_admin_bulk_upload_update(self):
        treasury = TreasuryFactory.create()
        url = reverse("treasury-admin-bulk-upload")
        treasury_data = [
            {
                "id": treasury.id,
                **TreasuriesTestCase.treasury,
            }
        ]
        for key, value in treasury_data[0].items():
            if key != "id":
                self.assertNotEqual(getattr(treasury, key), value)
        response = TreasuriesTestCase.client.post(url, treasury_data, format="json")
        modified_treasury = response.data["modified_treasuries"][0]
        for key, value in treasury_data[0].items():
            self.assertEqual(modified_treasury[key], value)

    def test_admin_bulk_upload_invalid_id(self):
        treasury = TreasuryFactory.create()
        url = reverse("treasury-admin-bulk-upload")
        treasury_data = [
            {
                "id": treasury.id + 1,
                **TreasuriesTestCase.treasury,
            }
        ]
        response = TreasuriesTestCase.client.post(url, treasury_data, format="json")
        self.assertEqual(
            response.data, {"error": "id should not be specified for new treasuries"}
        )

    def test_admin_bulk_upload_invalid_json(self):
        url = reverse("treasury-admin-bulk-upload")
        response = TreasuriesTestCase.client.post(url, "invalid json", format="json")
        self.assertEqual(
            response.data, {"error": "Invalid JSON format: expected list of treasuries"}
        )

    def test_admin_bulk_upload_no_data(self):
        url = reverse("treasury-admin-bulk-upload")
        response = TreasuriesTestCase.client.post(url, [], format="json")
        self.assertEqual(response.data, {"error": "No data provided"})

    def test_admin_bulk_upload_unique_exchange_and_symbol(self):
        url = reverse("treasury-admin-list")
        response = TreasuriesTestCase.client.post(
            url, TreasuriesTestCase.treasury, format="json"
        )
        url = reverse("treasury-admin-bulk-upload")
        treasury_data = [
            {
                **TreasuriesTestCase.treasury,
                "company": "NEWCOMPANYNAME",
            }
        ]
        response = TreasuriesTestCase.client.post(url, treasury_data, format="json")
        self.assertEqual(
            str(response.data["non_field_errors"][0]),
            "The fields exchange, symbol must make a unique set.",
        )

    def test_admin_bulk_upload_unique_company_name(self):
        url = reverse("treasury-admin-list")
        response = TreasuriesTestCase.client.post(
            url, TreasuriesTestCase.treasury, format="json"
        )
        url = reverse("treasury-admin-bulk-upload")
        treasury_data = [
            {
                **TreasuriesTestCase.treasury,
                "exchange": TreasuriesTestCase.treasury["exchange"],
                "symbol": "TSLATEST2",
            }
        ]
        response = TreasuriesTestCase.client.post(url, treasury_data, format="json")
        self.assertEqual(str(response.data["company"][0]), "This field must be unique.")

# User tests
    def test_get_treasuries(self):
        url = reverse("treasury-list")
        response = TreasuriesTestCase.client.get(url)

        treasuries = Treasury.objects.all()
        serializer = TreasurySerializer(treasuries, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_treasury(self):
        treasury = TreasuryFactory.create()
        url = reverse("treasury-detail", kwargs={"pk": treasury.pk})
        response = TreasuriesTestCase.client.get(url)

        treasury = Treasury.objects.get(pk=treasury.pk)
        serializer = TreasurySerializer(treasury)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        
    def test_get_treasury_not_found(self):
        max_id = Treasury.objects.all().aggregate(Max('id'))['id__max'] or 0
        non_existent_id = max_id + 1
        url = reverse("treasury-detail", kwargs={"pk": non_existent_id})
        response = TreasuriesTestCase.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# History tests
    def test_history(self):
        treasury = TreasuryFactory.create()
        history_url = reverse("treasury-history", kwargs={"pk": treasury.pk})
        response = TreasuriesTestCase.client.get(history_url)
        old_exchange = treasury.exchange
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["exchange"], old_exchange)
        self.assertEqual(len(response.data), 1)
        url = reverse("treasury-admin-detail", kwargs={"pk": treasury.pk})
        data = {"exchange": "NEW-EXCHANGE"}
        response = TreasuriesTestCase.client.patch(url, data, format="json")
        response = TreasuriesTestCase.client.get(history_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["exchange"], "NEW-EXCHANGE")
        self.assertEqual(len(response.data), 2)

    @patch("django.utils.timezone.now")
    def test_history_start(self, mock_now):
        mock_now.return_value = timezone.make_aware(datetime.datetime(2022, 1, 1))
        treasury = TreasuryFactory.create()
        history_url = reverse("treasury-history", kwargs={"pk": treasury.pk})
        url = reverse("treasury-admin-detail", kwargs={"pk": treasury.pk})
        data = {"exchange": "NEW-EXCHANGE"}
        mock_now.return_value = timezone.make_aware(datetime.datetime(2025, 1, 1))
        client = getAdminClient()
        response = client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = TreasuriesTestCase.client.get(history_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        response = TreasuriesTestCase.client.get(
            history_url, {"start": "20230101"}
        )  # Later date
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["exchange"], "NEW-EXCHANGE")
        
    @patch("django.utils.timezone.now")
    def test_history_end(self, mock_now):
        mock_now.return_value = timezone.make_aware(datetime.datetime(2022, 1, 1))
        treasury = TreasuryFactory.create()
        old_exchange = treasury.exchange
        history_url = reverse("treasury-history", kwargs={"pk": treasury.pk})
        url = reverse("treasury-admin-detail", kwargs={"pk": treasury.pk})
        data = {"exchange": "NEW-EXCHANGE"}
        mock_now.return_value = timezone.make_aware(datetime.datetime(2025, 1, 1))
        client = getAdminClient()
        response = client.patch(url, data, format="json")
        response = TreasuriesTestCase.client.get(history_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        response = TreasuriesTestCase.client.get(
            history_url, {"end": "20230101"}
        )  # Later date
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["exchange"], old_exchange)

    @patch("django.utils.timezone.now")
    def test_history_precise_range(self, mock_now):
        mock_now.return_value = timezone.make_aware(
            datetime.datetime(2022, 1, 1, 12, 30, 30)
        )
        treasury = TreasuryFactory.create()
        history_url = reverse("treasury-history", kwargs={"pk": treasury.pk})
        url = reverse("treasury-admin-detail", kwargs={"pk": treasury.pk})
        data = {"exchange": "NEW-EXCHANGE"}
        mock_now.return_value = timezone.make_aware(
            datetime.datetime(2022, 1, 1, 12, 30, 40)
        )
        client = getAdminClient()
        response = client.patch(url, data, format="json")
        response = TreasuriesTestCase.client.get(history_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        response = TreasuriesTestCase.client.get(
            history_url, {"start": "20220101123038", "end": "20220101123041"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["exchange"], "NEW-EXCHANGE")
