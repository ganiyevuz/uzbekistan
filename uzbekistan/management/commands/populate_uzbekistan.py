"""
Management command to populate Uzbekistan database with regions, districts, and villages.
"""

import yaml
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.conf import settings

from uzbekistan.models import Region, District, Village
from uzbekistan.dynamic_importer import DynamicImporter


class Command(BaseCommand):
    help = 'Populate Uzbekistan database with regions, districts, and villages'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force populate even if data already exists',
        )
        parser.add_argument(
            '--models',
            nargs='+',
            choices=['region', 'district', 'village'],
            help='Specific models to populate (default: all enabled models)',
        )

    def handle(self, *args, **options):
        """Handle the populate command."""
        force = options['force']
        specific_models = options.get('models')
        
        # Check if prepopulate is enabled
        prepopulate_enabled = DynamicImporter.get_setting('prepopulate', {}).get('enabled', False)
        if not prepopulate_enabled and not force:
            self.stdout.write(
                self.style.WARNING(
                    'Prepopulate is disabled in settings. Use --force to override.'
                )
            )
            return

        # Get enabled models
        enabled_models = DynamicImporter.get_enabled_items("models")
        if specific_models:
            models_to_populate = set(specific_models) & enabled_models
        else:
            models_to_populate = enabled_models

        if not models_to_populate:
            self.stdout.write(
                self.style.WARNING('No enabled models to populate.')
            )
            return

        self.stdout.write(f'Populating models: {", ".join(models_to_populate)}')

        try:
            with transaction.atomic():
                # Populate regions first
                if 'region' in models_to_populate:
                    self.populate_regions(force)
                
                # Populate districts
                if 'district' in models_to_populate:
                    self.populate_districts(force)
                
                # Populate villages
                if 'village' in models_to_populate:
                    self.populate_villages(force)

            self.stdout.write(
                self.style.SUCCESS('Successfully populated Uzbekistan database!')
            )
        except Exception as e:
            raise CommandError(f'Error populating database: {e}')

    def populate_regions(self, force=False):
        """Populate regions from YAML file."""
        if not force and Region.objects.exists():
            self.stdout.write(
                self.style.WARNING('Regions already exist. Use --force to override.')
            )
            return

        regions_file = Path(__file__).parent.parent.parent / 'fixtures' / 'regions.yaml'
        if not regions_file.exists():
            self.stdout.write(
                self.style.ERROR(f'Regions file not found: {regions_file}')
            )
            return

        with open(regions_file, 'r', encoding='utf-8') as f:
            regions_data = yaml.safe_load(f)

        if force:
            Region.objects.all().delete()

        created_count = 0
        for region_data in regions_data:
            region, created = Region.objects.get_or_create(
                name_uz=region_data['name_uz'],
                defaults={
                    'name_oz': region_data['name_oz'],
                    'name_ru': region_data['name_ru'],
                    'name_en': region_data['name_en'],
                }
            )
            if created:
                created_count += 1

        self.stdout.write(f'Created {created_count} regions')

    def populate_districts(self, force=False):
        """Populate districts from YAML file."""
        if not force and District.objects.exists():
            self.stdout.write(
                self.style.WARNING('Districts already exist. Use --force to override.')
            )
            return

        districts_file = Path(__file__).parent.parent.parent / 'fixtures' / 'districts.yaml'
        if not districts_file.exists():
            self.stdout.write(
                self.style.ERROR(f'Districts file not found: {districts_file}')
            )
            return

        with open(districts_file, 'r', encoding='utf-8') as f:
            districts_data = yaml.safe_load(f)

        if force:
            District.objects.all().delete()

        created_count = 0
        for district_data in districts_data:
            try:
                region = Region.objects.get(name_uz=district_data['region_name_uz'])
                district, created = District.objects.get_or_create(
                    name_uz=district_data['name_uz'],
                    region=region,
                    defaults={
                        'name_oz': district_data['name_oz'],
                        'name_ru': district_data['name_ru'],
                        'name_en': district_data.get('name_en', ''),
                    }
                )
                if created:
                    created_count += 1
            except Region.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f'Region not found for district: {district_data["name_uz"]}'
                    )
                )

        self.stdout.write(f'Created {created_count} districts')

    def populate_villages(self, force=False):
        """Populate villages from YAML file."""
        if not force and Village.objects.exists():
            self.stdout.write(
                self.style.WARNING('Villages already exist. Use --force to override.')
            )
            return

        # For now, we'll create a simple example village
        # In a real implementation, you'd load from a villages.yaml file
        if force:
            Village.objects.all().delete()

        created_count = 0
        # Get a sample district to create villages for
        sample_district = District.objects.first()
        if sample_district:
            sample_villages = [
                {
                    'name_uz': 'Mirobod',
                    'name_oz': 'Миробод',
                    'name_ru': 'Мирабад',
                },
                {
                    'name_uz': 'Yunusobod',
                    'name_oz': 'Юнусобод',
                    'name_ru': 'Юнусабад',
                }
            ]
            
            for village_data in sample_villages:
                village, created = Village.objects.get_or_create(
                    name_uz=village_data['name_uz'],
                    district=sample_district,
                    defaults={
                        'name_oz': village_data['name_oz'],
                        'name_ru': village_data['name_ru'],
                    }
                )
                if created:
                    created_count += 1

        self.stdout.write(f'Created {created_count} villages')
