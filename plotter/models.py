from django.db import models
from django.contrib.auth.models import User


class Study(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='studies',
        null=True)
    plot_cnt_wide = models.PositiveSmallIntegerField(null=False)
    plot_cnt_long = models.PositiveSmallIntegerField(null=False)
    plot_sz_wide = models.FloatField(null=False)
    plot_sz_long = models.FloatField(null=False)
    alley_dist_wide = models.FloatField(null=True)
    alley_dist_long = models.FloatField(null=True)

    metric = models.BooleanField()


    def __str__(self):
        return self.name


class Rep(models.Model):
    study = models.ForeignKey(Study, on_delete=models.PROTECT, related_name='reps')
    block = models.CharField(max_length=30, unique=False, default=1)
    rep_name = models.CharField(max_length=30, unique=True)
    lower_left_corner_y = models.FloatField(null=False, default=0)
    lower_left_corner_x = models.FloatField(null=False, default=0)
    upper_left_corner_y = models.FloatField(null=False, default=0)
    upper_left_corner_x = models.FloatField(null=False, default=0)

    def __str__(self):
        return "{study}: {rep}".format(study = self.study, rep = self.rep_name)