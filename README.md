# 🌍 Uzbekistan

[![PyPI Version](https://img.shields.io/pypi/v/uzbekistan)](https://pypi.org/project/uzbekistan/)
[![Django Version](https://img.shields.io/badge/Django-5.x-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Codecov status](https://codecov.io/gh/ganiyevuz/uzbekistan/graph/badge.svg?token=C8D9Q4GQCX)](https://codecov.io/gh/ganiyevuz/uzbekistan)

A comprehensive Django package providing complete database of Uzbekistan's Regions, Districts & Quarters with multi-language support including Latin, Cyrillic, and Russian versions.

## 📊 Database Overview

- **Regions**: 14
- **Regions/Cities**: 205
- **Towns/Districts**: 2,183+

## ✨ Features

- Complete database of Uzbekistan's Regions, Districts & Quarters
- Multi-language support:
  - Uzbek (Latin)
  - Uzbek (Cyrillic)
  - Russian
  - English
- REST API endpoints
- Configurable model activation
- Built-in caching
- Django Admin integration
- JSON serialization methods on all models

## 🚀 Quick Start

### Installation

```bash
pip install uzbekistan
```

### Basic Setup

1. Add to `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    ...
    'uzbekistan',
]
```

2. Configure in `settings.py`:
```python
UZBEKISTAN = {
    'models': {
        'region': True,  # Enable Region model
        'district': True,  # Enable District model
        'village': True,  # Enable Village model
    },
    'views': {
        'region': True,  # Enable RegionListAPIView
        'district': True,  # Enable DistrictListAPIView
        'village': True,  # Enable VillageListAPIView
    },
    'cache': {
        'enabled': True,  # Enable caching
        'timeout': 3600,  # Cache timeout (1 hour)
        'key_prefix': "uzbekistan"  # Cache key prefix
    },
    "use_authentication": False  # Disable authentication for API views (if needed)
}
```

3. Add URLs:
```python
urlpatterns = [
    path('', include('uzbekistan.urls')),
]
```

4. Run migrations (fixtures are loaded automatically on first migrate):
```bash
python manage.py makemigrations
python manage.py migrate
```

> Data is seeded automatically after migration if the tables are empty.
> Re-running `migrate` will **not** reload data that already exists.

### Management Commands

| Command | Description |
|---------|-------------|
| `python manage.py flush_uzbekistan` | Clear all Uzbekistan data (regions, districts, villages) |
| `python manage.py flush_uzbekistan --no-input` | Clear without confirmation prompt |

After flushing, the next `migrate` will re-seed the data automatically.

## 🔌 API Endpoints

### Available Endpoints

| Endpoint | URL Pattern | Name | Description |
|----------|-------------|------|-------------|
| Regions | `/regions` | `region-list` | List all regions |
| Districts | `/districts/<int:region_id>` | `district-list` | List districts for a specific region |
| Villages | `/villages/<int:district_id>` | `village-list` | List villages for a specific district |

### Example Usage

```python
# Get all regions
GET /regions

# Get districts for a specific region
GET /districts/1  # where 1 is the region_id

# Get villages for a specific district
GET /villages/1  # where 1 is the district_id
```

## 📋 JSON Serialization

All models provide an `as_json()` method for lightweight JSON-serializable output — useful outside of DRF views (e.g., management commands, Celery tasks, webhooks).

### Region

```python
region = Region.objects.get(pk=1)
region.as_json()
# {"id": 1, "name_uz": "Toshkent", "name_oz": "Тошкент", "name_ru": "Ташкент", "name_en": "Tashkent"}
```

### District

```python
district = District.objects.get(pk=1)

# Basic usage
district.as_json()
# {"id": 1, "name_uz": "Bekobod", "name_oz": "Бекобод", "name_ru": "Бекабад", "name_en": "Bekabad"}

# Include parent region
district.as_json(include_region=True)
# {"id": 1, "name_uz": "Bekobod", ..., "region": {"id": 1, "name_uz": "Toshkent", ...}}
```

### Village

```python
village = Village.objects.get(pk=1)

# Basic usage
village.as_json()
# {"id": 1, "name_uz": "Olmazar", "name_oz": "Олмазар", "name_ru": "Олмазар"}

# Include parent district
village.as_json(include_district=True)
# {"id": 1, ..., "district": {"id": 1, "name_uz": "Bekobod", ...}}

# Include both district and region
village.as_json(include_district=True, include_region=True)
# {"id": 1, ..., "district": {"id": 1, ..., "region": {"id": 1, ...}}}
```

## 🛠️ Development

### Setup

```bash
# Clone repository
git clone https://github.com/ganiyevuz/uzbekistan.git
cd uzbekistan

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"
```

### Development Tools

- **Testing**: `pytest`
- **Code Style**: 
  ```bash
  black --check uzbekistan/
  ```

## 📦 Release Process

### Automated Release

1. Update version:
```bash
python scripts/update_version.py 2.7.3
```

2. Create and push tag:
```bash
git tag v2.7.3
git push origin v2.7.3
```

GitHub Actions will automatically:
- Run tests
- Build package
- Publish to PyPI

### Manual Release

```bash
# Build package
python -m build

# Check package
twine check dist/*

# Upload to PyPI
twine upload dist/*
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## 👤 Author

Jakhongir Ganiev - [@ganiyevuz](https://github.com/ganiyevuz)

## 🙏 Acknowledgments

- All contributors who helped improve this package
- Django and DRF communities for their excellent tools and documentation