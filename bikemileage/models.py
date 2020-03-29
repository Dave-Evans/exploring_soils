from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Bicycle(models.Model):

    name = models.CharField(max_length=30, blank=False, null=False)
    make = models.CharField(max_length=30, default="Unknown")
    model = models.CharField(max_length=30, default="Unknown")
    year = models.PositiveSmallIntegerField(null=True, blank = True)
    owner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='bicycles',
        null=True)

    class Meta:
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse('bicycle_list')

    def __str__(self):
        return self.name


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

    ride_date   = models.DateField(null=False, blank=False)
    rider       = models.CharField(max_length=30, blank=True, null=True)
    mileage     = models.FloatField(null=True)
    # bike_type   = models.PositiveSmallIntegerField(choices=BIKE_TYPES)
    bike_type   = models.ForeignKey(Bicycle, models.PROTECT, related_name='mileage')
    comment     = models.TextField(blank=True, null=True)
    cost        = models.FloatField(null=True)

    def get_absolute_url(self):
        return reverse('custom_mileage')
        # TODO figure out how to redirect to a sorted page
        #, kwargs={'pk': self.pk})
        #sort=-ride_date
