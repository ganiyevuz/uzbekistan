from django.core.management.base import BaseCommand

from uzbekistan.dynamic_importer import DynamicImporter


class Command(BaseCommand):
    help = "Clear all Uzbekistan data (regions, districts, villages)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--no-input",
            action="store_true",
            dest="no_input",
            help="Skip confirmation prompt.",
        )

    def handle(self, *args, **options):
        from uzbekistan.models import Region, District, Village

        if not options["no_input"]:
            confirm = input(
                "This will delete ALL Uzbekistan data (regions, districts, villages). "
                "Are you sure? [y/N] "
            )
            if confirm.lower() != "y":
                self.stdout.write(self.style.WARNING("Aborted."))
                return

        deleted_total = 0
        for model_name, model in [
            ("village", Village),
            ("district", District),
            ("region", Region),
        ]:
            if DynamicImporter.is_model_enabled(model_name):
                count, _ = model.objects.all().delete()
                deleted_total += count
                self.stdout.write(f"  Deleted {count} {model_name}(s).")

        self.stdout.write(self.style.SUCCESS(f"Done. {deleted_total} records deleted."))
