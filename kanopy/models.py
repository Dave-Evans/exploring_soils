from django.db import models
from djgeojson.fields import PointField
from django.contrib.gis.db import models as geo_models

class Groundcoverdoc(models.Model):
    locname = models.CharField(max_length=255, blank=True)
    collectionpoint = geo_models.PointField(verbose_name="Collection Point", null=True)
    description = models.CharField(max_length=255, blank=True)
    image = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Samplepoint(geo_models.Model):
    description = models.CharField(max_length=255, blank=True)
    sampleloc = geo_models.PointField()