from django.db import models
from django.contrib.gis.db import models as geo_models


class CleanedData(models.Model):

    year = models.IntegerField(verbose_name="", null=True)
    farm = models.IntegerField(verbose_name="", null=True)
    field = models.IntegerField(verbose_name="", null=True)
    state = models.CharField(verbose_name="", null=True, max_length=250)
    county = models.CharField(verbose_name="", null=True, max_length=250)
    zipcode = models.IntegerField(verbose_name="", null=True)
    ag_yrs = models.CharField(verbose_name="", null=True, max_length=250)
    farmtype = models.CharField(verbose_name="", null=True, max_length=250)
    soil_texture = models.CharField(verbose_name="", null=True, max_length=250)
    topography = models.CharField(verbose_name="", null=True, max_length=250)
    standing_water = models.CharField(verbose_name="", null=True, max_length=250)
    poor_water_retention = models.CharField(verbose_name="", null=True, max_length=250)
    soilcover = models.CharField(verbose_name="", null=True, max_length=250)
    soilcover_norm = models.DecimalField(
        decimal_places=2, max_digits=15, verbose_name="", null=True
    )
    tillage_intensity_norm_v2 = models.DecimalField(
        decimal_places=2, max_digits=15, verbose_name="", null=True
    )
    rotation_div_norm = models.DecimalField(
        decimal_places=2, max_digits=15, verbose_name="", null=True
    )
    orgamend_norm = models.DecimalField(
        decimal_places=2, max_digits=15, verbose_name="", null=True
    )
    cc_history_norm = models.DecimalField(
        decimal_places=2, max_digits=15, verbose_name="", null=True
    )
    cc_div_norm = models.DecimalField(
        decimal_places=2, max_digits=15, verbose_name="", null=True
    )
    emi_v2 = models.DecimalField(
        decimal_places=2, max_digits=15, verbose_name="", null=True
    )
    cc_current_type = models.CharField(verbose_name="", null=True, max_length=250)
    cc_current_overwintering = models.CharField(
        verbose_name="", null=True, max_length=250
    )
    cc_current_rate_overwintering = models.CharField(
        verbose_name="", null=True, max_length=250
    )
    cc_current_winterkill = models.CharField(verbose_name="", null=True, max_length=250)
    cc_current_rate_winterkill = models.CharField(
        verbose_name="", null=True, max_length=250
    )
    fdiversity = models.DecimalField(
        decimal_places=2, max_digits=15, verbose_name="", null=True
    )
    richness = models.DecimalField(
        decimal_places=2, max_digits=15, verbose_name="", null=True
    )
    irrigation = models.CharField(verbose_name="", null=True, max_length=250)
    cc_plantstrat = models.CharField(verbose_name="", null=True, max_length=250)
    cc_plantdate = models.DateField(null=True)
    cc_sampledate = models.DateField(null=True)
    cc_area = models.DecimalField(
        decimal_places=2, max_digits=15, verbose_name="", null=True
    )
    pc = models.CharField(verbose_name="", null=True, max_length=250)
    sc = models.CharField(verbose_name="", null=True, max_length=250)
    cc_current_n = models.CharField(verbose_name="", null=True, max_length=250)
    cc_current_n_rate = models.DecimalField(
        decimal_places=2, max_digits=15, verbose_name="", null=True
    )
    cc_current_p = models.CharField(verbose_name="", null=True, max_length=250)
    cc_current_p_rate = models.DecimalField(
        decimal_places=2, max_digits=15, verbose_name="", null=True
    )
    cc_current_manure = models.CharField(verbose_name="", null=True, max_length=250)
    cc_current_manure_rate = models.DecimalField(
        decimal_places=2, max_digits=15, verbose_name="", null=True
    )
    cc_current_compost = models.CharField(verbose_name="", null=True, max_length=250)
    cc_current_compost_rate = models.DecimalField(
        decimal_places=2, max_digits=15, verbose_name="", null=True
    )
    pc_n = models.CharField(verbose_name="", null=True, max_length=250)
    pc_n_rate = models.DecimalField(
        decimal_places=2, max_digits=15, verbose_name="", null=True
    )
    pc_p = models.CharField(verbose_name="", null=True, max_length=250)
    pc_p_rate = models.DecimalField(
        decimal_places=2, max_digits=15, verbose_name="", null=True
    )
    pc_manure = models.CharField(verbose_name="", null=True, max_length=250)
    pc_manure_rate = models.DecimalField(
        decimal_places=2, max_digits=15, verbose_name="", null=True
    )
    pc_compost = models.CharField(verbose_name="", null=True, max_length=250)
    pc_compost_rate = models.DecimalField(
        decimal_places=2, max_digits=15, verbose_name="", null=True
    )
    gdd = models.DecimalField(
        decimal_places=2, max_digits=15, verbose_name="", null=True
    )
    precip = models.DecimalField(
        decimal_places=2, max_digits=15, verbose_name="", null=True
    )
    weedsuppression = models.DecimalField(
        decimal_places=2, max_digits=15, verbose_name="", null=True
    )
    percent_cover = models.DecimalField(
        decimal_places=2, max_digits=15, verbose_name="", null=True
    )
    agb = models.DecimalField(
        decimal_places=2, max_digits=15, verbose_name="", null=True
    )
    agbn = models.DecimalField(
        decimal_places=2, max_digits=15, verbose_name="", null=True
    )
    farm_location = geo_models.PointField(verbose_name="Location", null=True)
