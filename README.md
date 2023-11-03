# 🌍 Regions, Districts &amp; Quarters Database

[![PyPI Version](https://img.shields.io/pypi/v/uzbekistan)](https://pypi.org/project/uzbekistan/)
[![Django Version](https://img.shields.io/badge/Django-4.x-green.svg)](https://www.djangoproject.com/)

Full Database of Uzbekistan Regions, Districts &amp; Quarters with
Latin, Cyrillic and Russian versions.

## Insights

Total Regions : 14 <br>
Total Regions/Cities : 205 <br>
Total Towns/Districts : 2,183+ <br>

Last Updated On : 5th June 2022

## Installation

You can install your app via pip:

```bash
pip install uzbekistan
```

Add it to your Django project's INSTALLED_APPS:

```python3

INSTALLED_APPS = [
    # ...
    'uzbekistan',
]
```

Include URL Configuration in the Project's urls.py

```python
urlpatterns = [
    # ...
    path('', include('uzbekistan.urls'), name='uzbekistan'),
]
```

## Change logs

A new version available that includes many updates.

- Added **villages** table covering towns and districts has been added,
- Deprecated **Quarters** table (Available in MySQL and MSSQL backups),
- Added **Ko‘kdala tumani**
- etc...

## Suggestions / Feedbacks

```
Suggestions & Feedbacks are Most Welcome
```

That's all Folks. Enjoy😊!