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
    Get cache settings from configuration.

    Returns:
        Dictionary of cache settings
    """
    cache_settings = get_uzbekistan_setting("cache", {"enabled": True, "timeout": 3600})
    if cache_settings["enabled"]:
        try:
            cache.set(
                "healthy_check_uzbekistan", "alive", timeout=cache_settings["timeout"]
            )
            cache_data = cache.get("healthy_check_uzbekistan")
            cache.delete("healthy_check_uzbekistan")
            # Check if the cache is working correctly
            if cache_data != "alive":
                raise CacheIncorrectlyConfigured("Cache is not configured correctly.")
        except Exception as e:
            raise CacheIncorrectlyConfigured(e)
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

    # Get enabled items based on class type
    enabled_items = (
        get_enabled_views() if class_type == "views" else get_enabled_models()
    )

    # Get enabled models for dependency checking
    enabled_models = get_enabled_models()

    for item_name in enabled_items:
        try:
            # Construct class name (e.g., Region -> RegionListAPIView)
            class_name = f"{item_name.title()}ListAPIView"

            # Check if class exists in module
            if not hasattr(module, class_name):
                continue

            # Get the class
            cls = getattr(module, class_name)

            # Check if class has required attributes
            if not hasattr(cls, "model"):
                continue

            # Check if model is enabled
            model_name = cls.model.__name__.lower()
            if model_name not in enabled_models:
                continue

            # Check if view is enabled
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
