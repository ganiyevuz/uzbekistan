"""
Tests for uzbekistan app views.
"""

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from uzbekistan.models import Region, District, Village

class TestRegionAPI(APITestCase):
    def setUp(self):
        self.region = Region.objects.create(
            name_uz="Toshkent",
            name_oz="Тошкент",
            name_ru="Ташкент",
            name_en="Tashkent"
        )
        self.url = reverse('region-list')

    def test_list_regions(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name_uz'], "Toshkent")

    def test_list_regions_with_cache(self):
        with self.settings(UZBEKISTAN={
            'models': {'region': True, 'district': True, 'village': True},
            'views': {'region': True, 'district': True, 'village': True},
            'cache': {'enabled': True, 'timeout': 300}
        }):
            # First request - should cache
            response1 = self.client.get(self.url)
            self.assertEqual(response1.status_code, status.HTTP_200_OK)
            
            # Second request - should use cache
            response2 = self.client.get(self.url)
            self.assertEqual(response2.status_code, status.HTTP_200_OK)
            self.assertEqual(response2.data, response1.data)

class TestDistrictAPI(APITestCase):
    def setUp(self):
        self.region = Region.objects.create(
            name_uz="Toshkent",
            name_oz="Тошкент",
            name_ru="Ташкент",
            name_en="Tashkent"
        )
        self.district = District.objects.create(
            name_uz="Yunusobod",
            name_oz="Юнусобод",
            name_ru="Юнусабад",
            name_en="Yunusabad",
            region=self.region
        )
        self.url = reverse('district-list', args=[self.region.id])

    def test_list_districts(self):
        with self.settings(UZBEKISTAN={
            'models': {'region': True, 'district': True, 'village': True},
            'views': {'region': True, 'district': True, 'village': True}
        }):
            response = self.client.get(self.url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]['name_uz'], "Yunusobod")

class TestVillageAPI(APITestCase):
    def setUp(self):
        self.region = Region.objects.create(
            name_uz="Toshkent",
            name_oz="Тошкент",
            name_ru="Ташкент",
            name_en="Tashkent"
        )
        self.district = District.objects.create(
            name_uz="Yunusobod",
            name_oz="Юнусобод",
            name_ru="Юнусабад",
            name_en="Yunusabad",
            region=self.region
        )
        self.village = Village.objects.create(
            name_uz="Mirobod",
            name_oz="Миробод",
            name_ru="Мирабад",
            district=self.district
        )
        self.url = reverse('village-list', args=[self.district.id])

    def test_list_villages(self):
        with self.settings(UZBEKISTAN={
            'models': {'region': True, 'district': True, 'village': True},
            'views': {'region': True, 'district': True, 'village': True}
        }):
            response = self.client.get(self.url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]['name_uz'], "Mirobod") 