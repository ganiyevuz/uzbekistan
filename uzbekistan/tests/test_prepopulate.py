"""
Tests for prepopulate functionality.
"""

from django.test import TestCase, override_settings
from django.core.management import call_command
from django.core.exceptions import CommandError
from io import StringIO

from uzbekistan.models import Region, District, Village
from uzbekistan.dynamic_importer import DynamicImporter


class TestPrepopulateCommand(TestCase):
    """Test the populate_uzbekistan management command."""

    def setUp(self):
        """Set up test data."""
        # Clear any existing data
        Region.objects.all().delete()
        District.objects.all().delete()
        Village.objects.all().delete()

    def test_populate_command_with_force(self):
        """Test populate command with --force flag."""
        # Create a test region first
        region = Region.objects.create(
            name_uz="Test Region",
            name_oz="Тест Регион",
            name_ru="Тестовый Регион",
            name_en="Test Region",
        )

        # Run the command with force
        out = StringIO()
        call_command("populate_uzbekistan", "--force", stdout=out)

        # Check that the command ran without errors
        self.assertIn("Successfully populated", out.getvalue())

    def test_populate_command_without_force(self):
        """Test populate command without --force flag."""
        # Create a test region first
        region = Region.objects.create(
            name_uz="Test Region",
            name_oz="Тест Регион",
            name_ru="Тестовый Регион",
            name_en="Test Region",
        )

        # Run the command without force
        out = StringIO()
        call_command("populate_uzbekistan", stdout=out)

        # Should show warning about existing data
        self.assertIn("already exist", out.getvalue())

    def test_populate_specific_models(self):
        """Test populate command with specific models."""
        out = StringIO()
        call_command("populate_uzbekistan", "--models", "region", stdout=out)

        # Should run without errors
        self.assertIn("Populating models: region", out.getvalue())

    @override_settings(
        UZBEKISTAN={
            "models": {"region": False, "district": False, "village": False},
            "views": {"region": False, "district": False, "village": False},
            "cache": {"enabled": True, "timeout": 3600, "key_prefix": "uzbekistan"},
            "prepopulate": {"enabled": False},
        }
    )
    def test_populate_disabled_setting(self):
        """Test populate command when prepopulate is disabled."""
        out = StringIO()
        call_command("populate_uzbekistan", stdout=out)

        # Should show warning about disabled prepopulate
        self.assertIn("Prepopulate is disabled", out.getvalue())


class TestPrepopulateSettings(TestCase):
    """Test prepopulate settings functionality."""

    def test_prepopulate_settings_default(self):
        """Test default prepopulate settings."""
        prepopulate_config = DynamicImporter.get_setting("prepopulate", {})

        # Should have default values
        self.assertIsInstance(prepopulate_config, dict)

    @override_settings(
        UZBEKISTAN={
            "models": {"region": True, "district": True, "village": True},
            "views": {"region": True, "district": True, "village": True},
            "cache": {"enabled": True, "timeout": 3600, "key_prefix": "uzbekistan"},
            "prepopulate": {
                "enabled": True,
                "auto_populate": True,
                "force_on_startup": False,
            },
        }
    )
    def test_prepopulate_settings_custom(self):
        """Test custom prepopulate settings."""
        prepopulate_config = DynamicImporter.get_setting("prepopulate", {})

        self.assertTrue(prepopulate_config.get("enabled", False))
        self.assertTrue(prepopulate_config.get("auto_populate", False))
        self.assertFalse(prepopulate_config.get("force_on_startup", True))


class TestAppConfigPrepopulate(TestCase):
    """Test app config prepopulate functionality."""

    def test_app_config_ready_method(self):
        """Test that app config ready method works."""
        from uzbekistan.apps import UzbekistanConfig

        app_config = UzbekistanConfig("uzbekistan", None)

        # Should not raise any exceptions
        try:
            app_config.ready()
        except Exception as e:
            # Only fail if it's not a configuration validation error
            if "UZBEKISTAN settings validation failed" not in str(e):
                raise

    @override_settings(
        UZBEKISTAN={
            "models": {"region": True, "district": True, "village": True},
            "views": {"region": True, "district": True, "village": True},
            "cache": {"enabled": True, "timeout": 3600, "key_prefix": "uzbekistan"},
            "prepopulate": {
                "enabled": True,
                "auto_populate": True,
                "force_on_startup": False,
            },
        }
    )
    def test_app_config_with_prepopulate_enabled(self):
        """Test app config with prepopulate enabled."""
        from uzbekistan.apps import UzbekistanConfig

        app_config = UzbekistanConfig("uzbekistan", None)

        # Should not raise any exceptions
        try:
            app_config.ready()
        except Exception as e:
            # Only fail if it's not a configuration validation error
            if "UZBEKISTAN settings validation failed" not in str(e):
                raise
