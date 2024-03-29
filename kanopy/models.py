from django.db import models
from djgeojson.fields import PointField
from django.contrib.gis.db import models as geo_models
from exploring_soils.storage_backends import PrivateMediaStorage
from .gdd_calc import calc_gdd


class CoverCrops(models.TextChoices):
    """Different Cover crops from which to choose"""

    NONE = None, "----------"
    ALFALFA = "ALFALFA", "Alfalfa (Medicago sativa)"
    ANNUAL_RYE = "ANNUAL_RYE", "Annual Rye (Lolium multiflorum)"
    BALANSA_CLOVER = "BALANSA_CLOVER", "Balansa clover (Trifolium michelianum Savi)"
    BARLEY = "BARLEY", "Barley"
    BERSEEM_CLOVER = "BERSEEM_CLOVER", "Berseem clover (Trifolium alexandrinum)"
    BUCKWHEAT = "BUCKWHEAT", "Buckweat (Fagopyrum esculentum)"
    CABBAGE = "CABBAGE", "Cabbage"
    CAMELINA = "CAMELINA", "Camelina (Camelina sativa)"
    CEREAL_RYE = "CEREAL_RYE", "Cereal Rye (Secale cereale)"
    COWPEAS = "COWPEAS", "Cowpeas (Vigna unguiculata)"
    CRIMSON_CLOVER = "CRIMSON_CLOVER", "Crimson clover (Trifolium incarnatum)"
    FIELD_PEAS = "FIELD_PEAS", "Field peas"
    FLAX = "FLAX", "Flax"
    HAIRY_VETCH = "HAIRY_VETCH", "Hairy vetch (Vicia villosa)"
    ITALIAN_RYEGRASS = "ITALIAN_RYEGRASS", "Italian ryegrass"
    KALE = "KALE", "Kale"
    LENTILS = "LENTILS", "Lentils"
    MILLET = "MILLET", "(Pearl) Millet"
    MUSTARDS = "MUSTARDS", "Mustards (Brassicaceae)"
    OATS = "OATS", "Oats (Avena sativa)"
    PENNYCRESS = "PENNYCRESS", "Pennycress (Thlaspi arvense)"
    RADISH = "RADISH", "Radish (Raphanus sativus)"
    RAPESEED = "RAPESEED", "Rapeseed (Brassica napus)"
    RED_CLOVER = "RED_CLOVER", "Red clover (Trifolium pratense)"
    SPRING_WHEAT = "SPRING_WHEAT", "Spring wheat"
    SUDANGRASS = "SUDANGRASS", "Sudangrass"
    SUNFLOWER = "SUNFLOWER", "Sunflower"
    SUNN_HEMP = "SUNN_HEMP", "Sunn Hemp (Crotalaria juncea)"
    TURNIP = "TURNIP", "Turnip (Brassica rapa var. rapa)"
    WHITE_CLOVER = "WHITE_CLOVER", "White clover (Trifolium repens)"
    WINTER_TRITICALE = "WINTER TRITICALE", "Winter Triticale (Triticosecale sp.)"
    WINTER_BARLEY = "WINTER_BARLEY", "Winter Barley"
    OTHER = "OTHER", "Other"


class SeedingMethod(models.TextChoices):
    """Different seeding methods"""

    DRILL = "DRILL", "Drill"
    BROADCAST = "BROADCAST", "Broadcast"
    BROADCAST_INCORPORATION = "BROADCAST_INCORPORATION", "Broadcast plus incorporation"
    AERIAL = "AERIAL", "Aerial"
    MANURE_SLURRY = "MANURE_SLURRY", "Manure slurry"
    OTHER = "OTHER", "Other"


class CashCrops(models.TextChoices):
    """Different cash crops"""

    CORN = "CORN", "Corn"
    CORN_SILAGE = "CORN_SILAGE", "Corn silage"
    SOY_BEANS = "SOY_BEANS", "Soy beans"
    SMALL_GRAIN = "SMALL_GRAIN", "Small grain"
    CANNING_CROP = "CANNING_CROP", "Canning crop"
    POTATOES = "POTATOES", "Potatoes"
    DRY_BEANS = "DRY_BEANS", "Dry beans"
    SUGAR_BEETS = "SUGAR_BEETS", "Sugar beets"
    PREVENT_PLANT = "PREVENT_PLANT", "Prevent plant"
    OTHER = "OTHER", "Other"


class Groundcoverdoc(models.Model):

    location_name = models.CharField(max_length=250, blank=True)

    collectionpoint = geo_models.PointField(verbose_name="Collection Point", null=True)

    photo_taken_date = models.DateField(null=False)
    image = models.ImageField(storage=PrivateMediaStorage())
    uploaded_at = models.DateTimeField(auto_now_add=True)
    fgcc_value = models.DecimalField(max_digits=10, decimal_places=7, blank=True)

    cover_crop_species_1 = models.CharField(max_length=25, choices=CoverCrops.choices)

    cover_crop_species_2 = models.CharField(
        max_length=25, choices=CoverCrops.choices, blank=True
    )
    cover_crop_species_3 = models.CharField(
        max_length=25, choices=CoverCrops.choices, blank=True
    )
    cover_crop_species_4 = models.CharField(
        max_length=25, choices=CoverCrops.choices, blank=True
    )

    cover_crop_planting_date = models.DateField()

    cover_crop_termination_date = models.DateField(null=True)

    cover_crop_planting_rate = models.FloatField(help_text="in pounds per acre")

    crop_prior = models.CharField(
        verbose_name="Cash crop planted prior",
        max_length=25,
        choices=CashCrops.choices,
        blank=True,
    )
    crop_posterior = models.CharField(
        verbose_name="Cash crop to be planted after",
        max_length=25,
        choices=CashCrops.choices,
        blank=True,
    )
    cover_crop_interseeded = models.BooleanField(
        verbose_name="Was the cover crop interseeded?", null=True
    )

    seeding_method = models.CharField(
        verbose_name="Cover crop seeding method",
        max_length=55,
        choices=SeedingMethod.choices,
    )

    comments = models.TextField(blank=True)

    contact_email = models.EmailField(blank=True)

    gdd = models.DecimalField(
        verbose_name="Cumulative growing degree days",
        decimal_places=2,
        max_digits=15,
        null=True,
    )

    county_name = models.CharField(
        verbose_name="County of collection", max_length=50, null=True
    )

    def populate_gdd(self):

        self.gdd = calc_gdd(self)

    def populate_county(self):

        from django.db import connection

        id = self.id
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
            select mc.countyname 
            from kanopy_groundcoverdoc kg
            left join mn_counties mc
            on ST_Intersects(kg.collectionpoint, mc.shape)
            where kg.id = {id}"""
            )
            row = cursor.fetchone()

        self.county_name = row[0]

    class Meta:

        permissions = (("can_view_submissions", "Can view submissions"),)
