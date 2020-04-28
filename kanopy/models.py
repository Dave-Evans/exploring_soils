from django.db import models
from djgeojson.fields import PointField

class Groundcoverdoc(models.Model):
    locname = models.CharField(max_length=255, blank=True)
    latitude = models.SmallIntegerField()
    longitude = models.SmallIntegerField()
    collectionpoint = PointField(verbose_name="Collection Point", null=True)
    description = models.CharField(max_length=255, blank=True)
    image = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
