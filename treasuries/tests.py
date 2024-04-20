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
        
    def test_to_string(self):
        company = TreasuryFactory.create()
        self.assertEqual(str(company), f"{company.company}({company.exchange}:{company.symbol})")
        
    def test_post_treasury(self):
        url = reverse('treasury-list')
        treasury_data = {
            'company': 'Company',
            'country': 'Country',
            'symbol': 'Symbol',
            'exchange': 'Exchange',
            'filingurl': 'http://example.com',
            'btc': 1,
            'btcc': '1',
            'btc_source_dt': '2021-01-01',
            'tot_balance_sheet': 1,
            'treasury_type': 'Public',
            'dateoffirstbuy': '2021-01-01',
            'percentbtc': '4',
            'info_url': 'http://example.com',
            'cssclass': 'CSSClass'
        }
        response = self.client.post(url, treasury_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['company'], treasury_data['company'])
        self.assertEqual(response.data['country'], treasury_data['country'])
        self.assertEqual(response.data['symbol'], treasury_data['symbol'])
        self.assertEqual(response.data['exchange'], treasury_data['exchange'])
        self.assertEqual(response.data['filingurl'], treasury_data['filingurl'])
        self.assertEqual(response.data['btc'], treasury_data['btc'])
        self.assertEqual(response.data['btcc'], treasury_data['btcc'])
        self.assertEqual(response.data['btc_source_dt'], treasury_data['btc_source_dt'])
        self.assertEqual(response.data['tot_balance_sheet'], treasury_data['tot_balance_sheet'])
        self.assertEqual(response.data['treasury_type'], treasury_data['treasury_type'])
        self.assertEqual(response.data['dateoffirstbuy'], treasury_data['dateoffirstbuy'])
        self.assertEqual(response.data['percentbtc'], treasury_data['percentbtc'])
        self.assertEqual(response.data['info_url'], treasury_data['info_url'])
        self.assertEqual(response.data['cssclass'], treasury_data['cssclass'])

    def test_get_treasuries(self):
        url = reverse('treasury-list')
        response = self.client.get(url)

        treasuries = Treasury.objects.all()
        serializer = TreasurySerializer(treasuries, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        
    def test_get_treasury(self):
        company = TreasuryFactory.create()
        url = reverse('treasury-detail', kwargs={'pk': company.pk})
        response = self.client.get(url)

        treasury = Treasury.objects.get(pk=company.pk)
        serializer = TreasurySerializer(treasury)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        
    def test_patch_treasury(self):
        company = TreasuryFactory.create()
        url = reverse('treasury-detail', kwargs={'pk': company.pk})
        response = self.client.get(url)
        old_exchange = response.data['exchange']
        
        data = {'exchange': 'NEW-EXCHANGE'}
        response = self.client.patch(url, data, format='json')
        treasury = Treasury.objects.get(pk=company.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data['exchange'], old_exchange)
        self.assertEqual(response.data['exchange'], treasury.exchange)
        
    def test_delete_treasury(self):
        company = TreasuryFactory.create()
        url = reverse('treasury-detail', kwargs={'pk': company.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Treasury.objects.filter(pk=company.pk).count(), 0)
