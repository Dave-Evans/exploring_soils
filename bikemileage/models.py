from django.db import models
from django.urls import reverse

class Mileage(models.Model):
    # TODO Bike should be separate model class
    BLUE_TREK = 1
    RED_TREK = 2
    TAKARA = 3
    FUJI = 4
    OTHER = 6
    BIKE_TYPES = (
        (BLUE_TREK, 'Blue Trek'),
        (RED_TREK, 'Red Trek'),
        (TAKARA, 'Takara'),
        (FUJI, 'Fuji'),
        (OTHER, 'Other'),
    )

    ride_date       = models.DateField(null=False, blank=False)
    rider              = models.CharField(max_length=30, blank=True, null=True)
    mileage               = models.FloatField(null=True)
    bike_type           = models.PositiveSmallIntegerField(choices=BIKE_TYPES)
    comment         = models.TextField(blank=True, null=True)
    cost           = models.FloatField(null=True)

    def get_absolute_url(self):
        return reverse('custom_mileage')
        #, kwargs={'pk': self.pk})
        #sort=-ride_date
