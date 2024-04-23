from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from treasuries.models import Treasury
from treasuries.serializers import TreasurySerializer
from treasuries.factories import TreasuryFactory


class TreasuryViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.treasury = {
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

    def test_to_string(self):
        treasury = TreasuryFactory.create()
        self.assertEqual(
            str(treasury),
            f"{treasury.id}-{treasury.company}({treasury.exchange}:{treasury.symbol})",
        )

    def test_post_treasury(self):
        url = reverse("treasury-list")
        response = self.client.post(url, self.treasury, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["company"], self.treasury["company"])
        self.assertEqual(response.data["country"], self.treasury["country"])
        self.assertEqual(response.data["symbol"], self.treasury["symbol"])
        self.assertEqual(response.data["exchange"], self.treasury["exchange"])
        self.assertEqual(response.data["filingurl"], self.treasury["filingurl"])
        self.assertEqual(response.data["btc"], self.treasury["btc"])
        self.assertEqual(response.data["btcc"], self.treasury["btcc"])
        self.assertEqual(response.data["btc_source_dt"], self.treasury["btc_source_dt"])
        self.assertEqual(
            response.data["tot_balance_sheet"], self.treasury["tot_balance_sheet"]
        )
        self.assertEqual(response.data["treasury_type"], self.treasury["treasury_type"])
        self.assertEqual(
            response.data["dateoffirstbuy"], self.treasury["dateoffirstbuy"]
        )
        self.assertEqual(response.data["percentbtc"], self.treasury["percentbtc"])
        self.assertEqual(response.data["info_url"], self.treasury["info_url"])
        self.assertEqual(response.data["cssclass"], self.treasury["cssclass"])

    def test_get_treasuries(self):
        url = reverse("treasury-list")
        response = self.client.get(url)

        treasuries = Treasury.objects.all()
        serializer = TreasurySerializer(treasuries, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_treasury(self):
        treasury = TreasuryFactory.create()
        url = reverse("treasury-detail", kwargs={"pk": treasury.pk})
        response = self.client.get(url)

        treasury = Treasury.objects.get(pk=treasury.pk)
        serializer = TreasurySerializer(treasury)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_patch_treasury(self):
        treasury = TreasuryFactory.create()
        url = reverse("treasury-detail", kwargs={"pk": treasury.pk})
        response = self.client.get(url)
        old_exchange = response.data["exchange"]

        data = {"exchange": "NEW-EXCHANGE"}
        response = self.client.patch(url, data, format="json")
        treasury = Treasury.objects.get(pk=treasury.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data["exchange"], old_exchange)
        self.assertEqual(response.data["exchange"], treasury.exchange)

    def test_delete_treasury(self):
        treasury = TreasuryFactory.create()
        url = reverse("treasury-detail", kwargs={"pk": treasury.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Treasury.objects.filter(pk=treasury.pk).count(), 0)

    def test_bulk_upload(self):
        url = reverse("treasury-bulk-upload")
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
            self.treasury
        ]
        response = self.client.post(url, treasury_data, format="json")
        new_treasury = response.data["new_treasuries"][0]
        for key, value in treasury_data[0].items():
            self.assertEqual(new_treasury[key], value)
        new_treasury = response.data["new_treasuries"][1]
        for key, value in treasury_data[1].items():
            self.assertEqual(new_treasury[key], value)
            
    def test_bulk_upload_update(self):
        treasury = TreasuryFactory.create()
        url = reverse("treasury-bulk-upload")
        treasury_data = [
            {
                "id": treasury.id,
                **self.treasury,
            }
        ]
        for key, value in treasury_data[0].items():
            if key != "id":
                self.assertNotEqual(getattr(treasury, key), value)
        response = self.client.post(url, treasury_data, format="json")
        modified_treasury = response.data["modified_treasuries"][0]
        for key, value in treasury_data[0].items():
            self.assertEqual(modified_treasury[key], value)
            
    def test_bulk_upload_invalid_id(self):
        treasury = TreasuryFactory.create()
        url = reverse("treasury-bulk-upload")
        treasury_data = [
            {
                "id": treasury.id + 1,
                **self.treasury,
            }
        ]
        response = self.client.post(url, treasury_data, format="json")
        self.assertEqual(response.data, {"error": "id should not be specified for new treasuries"})
        
    def test_bulk_upload_invalid_json(self):
        url = reverse("treasury-bulk-upload")
        response = self.client.post(url, "invalid json", format="json")
        self.assertEqual(response.data, {"error": "Invalid JSON format: expected list of treasuries"})

    def test_bulk_upload_no_data(self):
        url = reverse("treasury-bulk-upload")
        response = self.client.post(url, [], format="json")
        self.assertEqual(response.data, {"error": "No data provided"})
        
    def test_bulk_upload_unique_exchange_and_symbol(self):
        url = reverse("treasury-list")
        response = self.client.post(url, self.treasury, format="json")
        url = reverse("treasury-bulk-upload")
        treasury_data = [
            {
                **self.treasury,
                "company": "NEWCOMPANYNAME",
            }
        ]
        response = self.client.post(url, treasury_data, format="json")
        self.assertEqual(str(response.data['non_field_errors'][0]), "The fields exchange, symbol must make a unique set.")
        
    def test_bulk_upload_unique_company_name(self):
        url = reverse("treasury-list")
        response = self.client.post(url, self.treasury, format="json")
        url = reverse("treasury-bulk-upload")
        treasury_data = [
            {
                **self.treasury,
                "exchange": self.treasury["exchange"],
                "symbol": "TSLATEST2",
            }
        ]
        response = self.client.post(url, treasury_data, format="json")
        self.assertEqual(str(response.data['company'][0]), "This field must be unique.")
        