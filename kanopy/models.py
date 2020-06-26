from django.db import models
from djgeojson.fields import PointField
from django.contrib.gis.db import models as geo_models

class Groundcoverdoc(models.Model):
    locname = models.CharField(max_length=255, blank=True)
    collectionpoint = geo_models.PointField(verbose_name="Collection Point", null=True)
    description = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    fgcc_value = models.DecimalField(max_digits=10, decimal_places=7, blank=True)

class Samplepoint(geo_models.Model):
    description = models.CharField(max_length=255, blank=True)
    sampleloc = geo_models.PointField()