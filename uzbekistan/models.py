from django.db.models import Model, CharField, ForeignKey, CASCADE


class Region(Model):
    name_uz = CharField(max_length=255)
    name_oz = CharField(max_length=255)
    name_ru = CharField(max_length=255)

    class Meta:
        db_table = 'regions'


class District(Model):
    name_uz = CharField(max_length=255)
    name_oz = CharField(max_length=255)
    name_ru = CharField(max_length=255)
    region = ForeignKey('uzbekistan.Region', on_delete=CASCADE)

    class Meta:
        db_table = 'districts'
