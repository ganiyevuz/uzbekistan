from functools import lru_cache
from importlib import import_module
from typing import Generator, Type, Any, Dict

from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured


class DynamicImportError(Exception):
    """Custom exception for dynamic import errors."""

    pass


class CacheIncorrectlyConfigured(Exception):
    """Custom exception for cache configuration errors."""

    pass


def get_uzbekistan_setting(setting_name: str, default: Any = None) -> Any:
    """
    Get a setting from UZBEKISTAN settings with proper error handling.

    Args:
        setting_name: Name of the setting to get
        default: Default value if setting doesn't exist

    Returns:
        The setting value or default

    Raises:
        ImproperlyConfigured: If UZBEKISTAN setting is not configured
    """
    if not hasattr(settings, "UZBEKISTAN") or settings.UZBEKISTAN is None:
        raise ImproperlyConfigured(
            "The UZBEKISTAN setting is required. Please add it to your settings.py file."
        )
    return settings.UZBEKISTAN.get(setting_name, default)


@lru_cache(maxsize=32)
def get_enabled_models() -> set:
    """
    Get set of enabled models from settings.
    Cached to avoid repeated dictionary lookups.

    Returns:
        Set of enabled model names
    """
    models = get_uzbekistan_setting("models", {})
    return {name.lower() for name, enabled in models.items() if enabled}


@lru_cache(maxsize=32)
def get_enabled_views() -> set:
    """
    Get set of enabled views from settings.
    Cached to avoid repeated dictionary lookups.

    Returns:
        Set of enabled view names
    """
    views = get_uzbekistan_setting("views", {})
    return {name.lower() for name, enabled in views.items() if enabled}


@lru_cache(maxsize=32)
def get_cache_settings() -> Dict[str, Any]:
    """
    Get cache settings from the configuration.

    Returns:
        Dictionary of cache settings
    """
    cache_settings = get_uzbekistan_setting("cache", {
        "enabled": True, 
        "timeout": 3600,
        "key_prefix": "uzbekistan"
    })
    if cache_settings["enabled"]:
        try:
            # Use a more efficient cache health check with prefix
            key_prefix = cache_settings.get("key_prefix", "uzbekistan")
            test_key = f"{key_prefix}_cache_health_check"
            test_value = "alive"
            cache.set(test_key, test_value, timeout=60)  # Short timeout for health check
            cache_data = cache.get(test_key)
            cache.delete(test_key)
            # Check if the cache is working correctly
            if cache_data != test_value:
                raise CacheIncorrectlyConfigured("Cache is not configured correctly.")
        except Exception as e:
            raise CacheIncorrectlyConfigured(f"Cache health check failed: {e}")
    return cache_settings


def import_conditional_classes(
    module_name: str, class_type: str
) -> Generator[Type[Any], None, None]:
    """
    Dynamically import classes based on settings configuration.

    Args:
        module_name: Full module path to import from
        class_type: Type of classes to import ('views' or 'models')

    Yields:
        Imported class objects

    Raises:
        DynamicImportError: If import fails or class not found
    """
    try:
        module = import_module(module_name)
    except ImportError as e:
        raise DynamicImportError(f"Failed to import module {module_name}: {str(e)}")

    # Get enabled items based on a class type (cached)
    enabled_items = (
        get_enabled_views() if class_type == "views" else get_enabled_models()
    )

    # Get enabled models for dependency checking (cached)
    enabled_models = get_enabled_models()

    # Pre-filter items to avoid unnecessary processing
    if not enabled_items:
        return

    for item_name in enabled_items:
        try:
            # Construct class name (e.g., Region -> RegionListAPIView)
            class_name = f"{item_name.title()}ListAPIView"

            # Check if class exists in module
            if not hasattr(module, class_name):
                continue

            # Get the class
            cls = getattr(module, class_name)

            # Check if a class has required attributes
            if not hasattr(cls, "model"):
                continue

            # Check if the model is enabled
            model_name = cls.model.__name__.lower()
            if model_name not in enabled_models:
                continue

            # For views, double-check if the view is enabled (redundant but safe)
            if class_type == "views" and item_name not in get_enabled_views():
                continue

            yield cls

        except AttributeError as e:
            raise DynamicImportError(
                f"Failed to import {class_name} from {module_name}: {str(e)}"
            )
        except Exception as e:
            raise DynamicImportError(
                f"Unexpected error importing {class_name} from {module_name}: {str(e)}"
            )
