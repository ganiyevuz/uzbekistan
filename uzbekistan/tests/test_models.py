"""
Tests for uzbekistan app models.
"""

import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from uzbekistan.models import Region, District, Village, check_model


class TestRegion(TestCase):
    def setUp(self):
        self.region = Region.objects.create(
            name_uz="Toshkent", name_oz="Тошкент", name_ru="Ташкент", name_en="Tashkent"
        )

    def test_region_creation(self):
        self.assertEqual(self.region.name_uz, "Toshkent")
        self.assertEqual(self.region.name_oz, "Тошкент")
        self.assertEqual(self.region.name_ru, "Ташкент")
        self.assertEqual(self.region.name_en, "Tashkent")

    def test_region_str(self):
        self.assertEqual(str(self.region), "Toshkent")

    def test_region_clean_validation(self):
        region = Region()
        with self.assertRaises(ValidationError):
            region.clean()


class TestDistrict(TestCase):
    def setUp(self):
        self.region = Region.objects.create(
            name_uz="Toshkent", name_oz="Тошкент", name_ru="Ташкент", name_en="Tashkent"
        )
        self.district = District.objects.create(
            name_uz="Yunusobod",
            name_oz="Юнусобод",
            name_ru="Юнусабад",
            name_en="Yunusabad",
            region=self.region,
        )

    def test_district_creation(self):
        self.assertEqual(self.district.name_uz, "Yunusobod")
        self.assertEqual(self.district.name_oz, "Юнусобод")
        self.assertEqual(self.district.name_ru, "Юнусабад")
        self.assertEqual(self.district.name_en, "Yunusabad")
        self.assertEqual(self.district.region, self.region)

    def test_district_str(self):
        self.assertEqual(str(self.district), "Yunusobod")

    def test_district_clean_validation(self):
        district = District()
        with self.assertRaises(ValidationError):
            district.clean()

    def test_district_region_name_property(self):
        self.assertEqual(self.district.region_name, "Toshkent")


class TestVillage(TestCase):
    def setUp(self):
        self.region = Region.objects.create(
            name_uz="Toshkent", name_oz="Тошкент", name_ru="Ташкент", name_en="Tashkent"
        )
        self.district = District.objects.create(
            name_uz="Yunusobod",
            name_oz="Юнусобод",
            name_ru="Юнусабад",
            name_en="Yunusabad",
            region=self.region,
        )
        self.village = Village.objects.create(
            name_uz="Mirobod",
            name_oz="Миробод",
            name_ru="Мирабад",
            district=self.district,
        )

    def test_village_creation(self):
        self.assertEqual(self.village.name_uz, "Mirobod")
        self.assertEqual(self.village.name_oz, "Миробод")
        self.assertEqual(self.village.name_ru, "Мирабад")
        self.assertEqual(self.village.district, self.district)

    def test_village_str(self):
        self.assertEqual(str(self.village), "Mirobod")

    def test_village_clean_validation(self):
        village = Village()
        with self.assertRaises(ValidationError):
            village.clean()

    def test_village_district_name_property(self):
        self.assertEqual(self.village.district_name, "Yunusobod")

    def test_village_region_name_property(self):
        self.assertEqual(self.village.region_name, "Toshkent")


class TestModelChecks(TestCase):
    def test_check_model_region(self):
        # Should not raise any exception since Region is enabled
        check_model(Region)

    def test_check_model_district(self):
        # Should not raise any exception since District and its dependency (Region) are enabled
        check_model(District)

    def test_check_model_village(self):
        # Should not raise any exception since Village and its dependencies (Region, District) are enabled
        check_model(Village)
