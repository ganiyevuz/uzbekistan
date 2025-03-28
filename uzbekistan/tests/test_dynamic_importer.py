"""
Tests for dynamic importer functionality.
"""

import pytest
from django.test import override_settings
from uzbekistan.dynamic_importer import (
    get_cache_settings,
    get_enabled_models,
    get_enabled_views,
    get_uzbekistan_setting,
    import_conditional_classes,
)


class TestDynamicImporter:
    def setup_method(self):
        """Clear cache before each test."""
        get_enabled_models.cache_clear()
        get_enabled_views.cache_clear()
        get_cache_settings.cache_clear()

    def test_get_enabled_models(self):
        """Test getting enabled models."""
        custom_settings = {
            'models': {'region': True, 'district': False, 'village': True}
        }
        with override_settings(UZBEKISTAN=custom_settings):
            enabled_models = get_enabled_models()
            assert enabled_models == {'region', 'village'}

    def test_get_enabled_views(self):
        """Test getting enabled views."""
        custom_settings = {
            'views': {'region': True, 'district': False, 'village': True}
        }
        with override_settings(UZBEKISTAN=custom_settings):
            enabled_views = get_enabled_views()
            assert enabled_views == {'region', 'village'}

    def test_get_cache_settings(self):
        """Test getting cache settings."""
        custom_settings = {
            'cache': {'enabled': True, 'timeout': 300}
        }
        with override_settings(UZBEKISTAN={'cache': custom_settings}):
            settings = get_cache_settings()
            assert settings == custom_settings

    def test_get_cache_settings_default(self):
        """Test getting default cache settings."""
        settings = get_cache_settings()
        assert settings == {'enabled': False, 'timeout': 3600}

    def test_get_uzbekistan_setting_missing(self):
        """Test getting missing setting."""
        with override_settings(UZBEKISTAN={}):
            value = get_uzbekistan_setting('missing_setting')
            assert value is None

    def test_get_uzbekistan_setting_with_default(self):
        """Test getting setting with default value."""
        with override_settings(UZBEKISTAN={}):
            value = get_uzbekistan_setting('missing_setting', default='default')
            assert value == 'default'

    def test_import_conditional_classes_success(self):
        """Test successful import of conditional classes."""
        with override_settings(UZBEKISTAN={
            'models': {'region': True, 'district': True, 'village': True},
            'views': {'region': True, 'district': True, 'village': True}
        }):
            views = list(import_conditional_classes('uzbekistan.views', 'views'))
            assert len(views) == 3
            assert all(hasattr(view, 'model') for view in views)

    def test_import_conditional_classes_disabled_model(self):
        """Test import with disabled model."""
        with override_settings(UZBEKISTAN={
            'models': {'region': True, 'district': False, 'village': True},
            'views': {'region': True, 'district': True, 'village': True}
        }):
            views = list(import_conditional_classes('uzbekistan.views', 'views'))
            assert len(views) == 2
            assert all(view.model.__name__.lower() != 'district' for view in views)

    def test_import_conditional_classes_invalid_module(self):
        """Test import with invalid module."""
        with pytest.raises(Exception):
            list(import_conditional_classes('invalid.module', 'views'))

    def test_import_conditional_classes_missing_class(self):
        """Test import with missing class."""
        with override_settings(UZBEKISTAN={
            'models': {'region': True, 'district': True, 'village': True},
            'views': {'region': True, 'district': True, 'village': True}
        }):
            views = list(import_conditional_classes('uzbekistan.views', 'views'))
            assert len(views) == 3 