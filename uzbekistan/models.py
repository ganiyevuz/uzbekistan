from django.db.models import Model, CharField, ForeignKey, CASCADE


class Region(Model):
    name_uz = CharField(max_length=255, unique=True)
    name_oz = CharField(max_length=255, unique=True)
    name_ru = CharField(max_length=255, unique=True)
    name_en = CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'regions'

    def __str__(self):
        return self.name_uz


class District(Model):
    name_uz = CharField(max_length=255)
    name_oz = CharField(max_length=255)
    name_ru = CharField(max_length=255)
    region = ForeignKey('uzbekistan.Region', on_delete=CASCADE)

    class Meta:
        db_table = 'districts'
        unique_together = ('name_uz', 'name_oz', 'name_ru', 'region')

    def __str__(self):
        return self.name_uz
