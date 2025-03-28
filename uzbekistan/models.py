from django.conf import settings
from django.db.models import Model, CharField, ForeignKey, CASCADE, Index
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from uzbekistan.dynamic_importer import get_uzbekistan_setting

# Language code validator
language_code_validator = RegexValidator(
    regex="^[a-z]{2}$",
    message=_("Language code must be 2 lowercase letters (e.g., uz, ru, en)"),
)


class Region(Model):
    name_uz = CharField(
        max_length=255,
        unique=True,
        db_index=True,
        help_text=_("Name in Uzbek language"),
    )
    name_oz = CharField(
        max_length=255,
        unique=True,
        db_index=True,
        help_text=_("Name in Uzbek Cyrillic"),
    )
    name_ru = CharField(
        max_length=255,
        unique=True,
        db_index=True,
        help_text=_("Name in Russian language"),
    )
    name_en = CharField(
        max_length=255,
        unique=True,
        db_index=True,
        help_text=_("Name in English language"),
    )

    class Meta:
        db_table = "regions"
        indexes = [
            Index(fields=["name_uz"]),
            Index(fields=["name_oz"]),
            Index(fields=["name_ru"]),
            Index(fields=["name_en"]),
        ]
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")

    def __str__(self):
        return self.name_uz

    def clean(self):
        """Validate that at least one name is provided."""
        if not any([self.name_uz, self.name_oz, self.name_ru, self.name_en]):
            raise ValueError(_("At least one name must be provided"))


class District(Model):
    name_uz = CharField(
        max_length=255, db_index=True, help_text=_("Name in Uzbek language")
    )
    name_oz = CharField(
        max_length=255, db_index=True, help_text=_("Name in Uzbek Cyrillic")
    )
    name_ru = CharField(
        max_length=255, db_index=True, help_text=_("Name in Russian language")
    )
    name_en = CharField(
        max_length=255,
        null=True,
        blank=True,
        db_index=True,
        help_text=_("Name in English language"),
    )
    region = ForeignKey(
        "uzbekistan.Region", on_delete=CASCADE, db_index=True, related_name="districts"
    )

    class Meta:
        db_table = "districts"
        unique_together = ("name_uz", "name_oz", "name_ru", "region")
        indexes = [
            Index(fields=["name_uz"]),
            Index(fields=["name_oz"]),
            Index(fields=["name_ru"]),
            Index(fields=["name_en"]),
            Index(fields=["region"]),
        ]
        verbose_name = _("District")
        verbose_name_plural = _("Districts")

    def __str__(self):
        return self.name_uz

    def clean(self):
        """Validate that at least one name is provided."""
        if not any([self.name_uz, self.name_oz, self.name_ru, self.name_en]):
            raise ValueError(_("At least one name must be provided"))

    @property
    def region_name(self):
        """Get the name of the related region."""
        return self.region.name_uz


class Village(Model):
    name_uz = CharField(
        max_length=255, db_index=True, help_text=_("Name in Uzbek language")
    )
    name_oz = CharField(
        max_length=255, db_index=True, help_text=_("Name in Uzbek Cyrillic")
    )
    name_ru = CharField(
        max_length=255, db_index=True, help_text=_("Name in Russian language")
    )
    district = ForeignKey(
        "uzbekistan.District", on_delete=CASCADE, db_index=True, related_name="villages"
    )

    class Meta:
        db_table = "villages"
        unique_together = ("name_uz", "name_oz", "name_ru", "district")
        indexes = [
            Index(fields=["name_uz"]),
            Index(fields=["name_oz"]),
            Index(fields=["name_ru"]),
            Index(fields=["district"]),
        ]
        verbose_name = _("Village")
        verbose_name_plural = _("Villages")

    def __str__(self):
        return self.name_uz

    def clean(self):
        """Validate that at least one name is provided."""
        if not any([self.name_uz, self.name_oz, self.name_ru]):
            raise ValueError(_("At least one name must be provided"))

    @property
    def district_name(self):
        """Get the name of the related district."""
        return self.district.name_uz

    @property
    def region_name(self):
        """Get the name of the related region."""
        return self.district.region_name


def check_model(model):
    """Check if the model is enabled in settings and its dependencies are met."""
    model_name = model.__name__.lower()

    # Get enabled models from settings
    enabled_models = get_uzbekistan_setting("models", {})

    if model._meta.abstract or not enabled_models.get(model_name, False):
        raise NotImplementedError(
            f"The model '{model}' is not enabled in the current configuration. "
            "Please check that this model is set to True in the 'models' dictionary "
            "of the UZBEKISTAN setting in your settings.py file."
        )

    # Check dependencies
    dependencies = {"district": ["region"], "village": ["region", "district"]}

    if model_name in dependencies:
        for dep in dependencies[model_name]:
            if not enabled_models.get(dep, False):
                raise NotImplementedError(
                    f"The '{model.__name__}' model requires the '{dep.title()}' model to be enabled. "
                    "Please ensure that '{dep.title()}' is set to True in the 'models' dictionary "
                    "of the UZBEKISTAN setting in your settings.py file."
                )
