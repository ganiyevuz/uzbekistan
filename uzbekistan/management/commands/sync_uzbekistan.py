from pathlib import Path

from django.core.management.base import BaseCommand
from django.core.serializers import deserialize

from uzbekistan.dynamic_importer import DynamicImporter


class Command(BaseCommand):
    help = "Sync Uzbekistan data: add missing fixture entries without modifying existing ones."

    FIXTURES_DIR = Path(__file__).resolve().parent.parent.parent / "fixtures"

    def handle(self, *args, **options):
        from uzbekistan.models import Region, District

        created_total = 0

        if DynamicImporter.is_model_enabled("region"):
            created = self._sync_fixture("regions.yaml", Region)
            created_total += created
            self.stdout.write(f"  Regions: {created} added.")

        if DynamicImporter.is_model_enabled("district"):
            created = self._sync_fixture("districts.yaml", District)
            created_total += created
            self.stdout.write(f"  Districts: {created} added.")

        self.stdout.write(
            self.style.SUCCESS(f"Done. {created_total} new records added.")
        )

    def _sync_fixture(self, fixture_file, model):
        fixture_path = self.FIXTURES_DIR / fixture_file
        existing_pks = set(model.objects.values_list("pk", flat=True))

        with open(fixture_path) as f:
            to_create = [
                obj.object
                for obj in deserialize("yaml", f)
                if obj.object.pk not in existing_pks
            ]

        if to_create:
            model.objects.bulk_create(to_create)

        return len(to_create)
