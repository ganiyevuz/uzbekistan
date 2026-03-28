"""
Tests for uzbekistan management commands.
"""

from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase, TransactionTestCase

from uzbekistan.models import Region, District


class TestFlushUzbekistan(TestCase):
    def setUp(self):
        self.region = Region.objects.create(
            name_uz="Toshkent", name_oz="Тошкент", name_ru="Ташкент", name_en="Tashkent"
        )
        self.district = District.objects.create(
            name_uz="Bekobod",
            name_oz="Бекобод",
            name_ru="Бекабад",
            name_en="Bekabad",
            region=self.region,
        )

    def test_flush_with_no_input(self):
        out = StringIO()
        call_command("flush_uzbekistan", "--no-input", stdout=out)
        output = out.getvalue()

        self.assertIn("Deleted", output)
        self.assertEqual(Region.objects.count(), 0)
        self.assertEqual(District.objects.count(), 0)

    def test_flush_aborted_on_decline(self):
        out = StringIO()
        with patch("builtins.input", return_value="n"):
            call_command("flush_uzbekistan", stdout=out)

        self.assertIn("Aborted", out.getvalue())
        self.assertEqual(Region.objects.count(), 1)

    def test_flush_confirmed(self):
        out = StringIO()
        with patch("builtins.input", return_value="y"):
            call_command("flush_uzbekistan", stdout=out)

        self.assertEqual(Region.objects.count(), 0)
        self.assertEqual(District.objects.count(), 0)


class TestSyncUzbekistan(TransactionTestCase):
    def test_sync_loads_fixtures_into_empty_db(self):
        out = StringIO()
        call_command("sync_uzbekistan", stdout=out)
        output = out.getvalue()

        self.assertGreater(Region.objects.count(), 0)
        self.assertGreater(District.objects.count(), 0)
        self.assertIn("added", output)

    def test_sync_skips_existing_data(self):
        out = StringIO()
        call_command("sync_uzbekistan", stdout=out)
        first_region_count = Region.objects.count()
        first_district_count = District.objects.count()

        out = StringIO()
        call_command("sync_uzbekistan", stdout=out)

        self.assertEqual(Region.objects.count(), first_region_count)
        self.assertEqual(District.objects.count(), first_district_count)
        self.assertIn("Regions: 0 added", out.getvalue())
        self.assertIn("Districts: 0 added", out.getvalue())

    def test_sync_adds_only_missing(self):
        out = StringIO()
        call_command("sync_uzbekistan", stdout=out)
        total_regions = Region.objects.count()

        # Delete one region and its districts
        region = Region.objects.first()
        region_pk = region.pk
        District.objects.filter(region=region).delete()
        region.delete()

        out = StringIO()
        call_command("sync_uzbekistan", stdout=out)

        self.assertEqual(Region.objects.count(), total_regions)
        self.assertTrue(Region.objects.filter(pk=region_pk).exists())
        self.assertIn("Regions: 1 added", out.getvalue())


class TestAutoSeed(TestCase):
    def test_seed_loads_on_empty_tables(self):
        """Verify seed_uzbekistan loads fixtures when tables are empty."""
        from uzbekistan.apps import seed_uzbekistan

        self.assertEqual(Region.objects.count(), 0)

        with self.settings(
            UZBEKISTAN={
                "models": {"region": True, "district": True, "village": True},
                "views": {"region": True, "district": True, "village": True},
                "cache": {"enabled": False, "timeout": 3600},
                "auto_seed": True,
            }
        ):
            seed_uzbekistan(sender=None)

        self.assertGreater(Region.objects.count(), 0)
        self.assertGreater(District.objects.count(), 0)

    def test_seed_skips_when_disabled(self):
        """Verify auto_seed=False prevents auto-loading."""
        from uzbekistan.apps import seed_uzbekistan

        self.assertEqual(Region.objects.count(), 0)

        with self.settings(
            UZBEKISTAN={
                "models": {"region": True, "district": True, "village": True},
                "views": {"region": True, "district": True, "village": True},
                "cache": {"enabled": False, "timeout": 3600},
                "auto_seed": False,
            }
        ):
            seed_uzbekistan(sender=None)

        self.assertEqual(Region.objects.count(), 0)

    def test_seed_skips_when_data_exists(self):
        """Verify seed doesn't reload when data already present."""
        from uzbekistan.apps import seed_uzbekistan

        # Load full fixtures first, then modify one region
        seed_uzbekistan.__wrapped__ = None  # just call directly
        with self.settings(
            UZBEKISTAN={
                "models": {"region": True, "district": True, "village": True},
                "views": {"region": True, "district": True, "village": True},
                "cache": {"enabled": False, "timeout": 3600},
                "auto_seed": True,
            }
        ):
            seed_uzbekistan(sender=None)

        # Modify a region name
        region = Region.objects.get(pk=1)
        region.name_uz = "Modified"
        region.save()

        # Re-run seed — should skip because tables are not empty
        with self.settings(
            UZBEKISTAN={
                "models": {"region": True, "district": True, "village": True},
                "views": {"region": True, "district": True, "village": True},
                "cache": {"enabled": False, "timeout": 3600},
                "auto_seed": True,
            }
        ):
            seed_uzbekistan(sender=None)

        # Should keep modified data, not overwrite with fixtures
        self.assertEqual(Region.objects.get(pk=1).name_uz, "Modified")
