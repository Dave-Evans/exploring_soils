from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.gis.db import models as geo_models
from .derive_species_class import derive_species_class
from exploring_soils.storage_backends import WiscCCPhotoStorage


# For making User's email non-unique
User._meta.get_field("email")._unique = True


class StateAbrevChoices(models.TextChoices):
    """In case someone doesn't exactly in WI"""

    WI = "WI", "WI"
    MN = "MN", "MN"
    IL = "IL", "IL"
    MI = "MI", "MI"
    IA = "IA", "IA"


class Farmer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250, blank=True)
    last_name = models.CharField(max_length=250, blank=True)
    farm_name = models.CharField(max_length=250, blank=True)
    county = models.TextField(verbose_name="County of farm", null=True)
    address_street = models.CharField(max_length=250, blank=True)
    address_municipality = models.CharField(max_length=250, blank=True)
    address_state = models.CharField(
        choices=StateAbrevChoices.choices,
        default=StateAbrevChoices.WI,
        max_length=2,
        null=True,
    )
    address_zipcode = models.PositiveIntegerField(
        null=True, validators=[MaxValueValidator(99999), MinValueValidator(1)]
    )

    phone_number = models.CharField(max_length=13, blank=True)


class NutrientMgmtSourcesChoices(models.TextChoices):
    """Different Nutrient management information sources"""

    BLANK = "", ""
    AGRONOMIST = "AGRONOMIST", "Agronomist/CCA/other private consultant"
    NEIGHBORS = "NEIGHBORS", "Friends and neighbor farmers"
    LOCAL_COOP = "LOCAL_COOP", "Local cooperative"
    LCO = "LCO", "Land conservation office"
    WATERSHED_GROUP = "WATERSHED_GROUP", "Producer-led Watershed Group"
    UW_EX = "UW_EX", "UW Extension"
    OTHER = "OTHER", "Other"


class CoverCropInfoSourcesChoices(models.TextChoices):
    """Different choices for cover crop information"""

    BLANK = "", ""
    AGRONOMIST = "AGRONOMIST", "Agronomist/CCA/other private consultant"
    NEIGHBORS = "NEIGHBORS", "Friends and neighbor farmers"
    LCO = "LCO", "Land conservation office"
    MICHAEL_FIELDS = "MICHAEL_FIELDS", "Michael Fields Agricultural Institute"
    MIDWEST_COV_CROPS_COUNCIL = (
        "MIDWEST_COV_CROPS_COUNCIL",
        "Midwest Cover Crop Council",
    )
    OGRAIN = "OGRAIN", "OGRAIN"
    PRACT_FARMS_IOWA = "PRACT_FARMS_IOWA", "Practical Farmers of Iowa"
    WATERSHED_GROUP = "WATERSHED_GROUP", "Producer-led Watershed Group"
    SEED_DEALER = "SEED_DEALER", "Seed Dealer"
    SOCIAL_MEDIA = "SOCIAL_MEDIA", "Social Media (Youtube, podcasts, etc)"
    UW_EX = "UW_EX", "UW Extension"
    OTHER = "OTHER", "Other"


class CoverCropSupportChoices(models.TextChoices):
    """In terms of support for cover cropping, select and rank the top 1 to 3 factors you’d like to see more of"""

    BLANK = "", ""
    ADDTL_UWEX = "ADDTL_UWEX", "Additional extension or agency personnel in your county"
    COST_SHARE = "COST_SHARE", "Cost sharing for cover cropping"
    COST_REDUCT = (
        "COST_REDUCT",
        "Cost reduction for the next cash crop (due to N credits, weed suppression, etc.)",
    )
    MORE_NEIGHBORS = "MORE_NEIGHBORS", "More neighbors using cover crops"
    MORE_INFO_ADAPT_EQUIP = (
        "MORE_INFO_ADAPT_EQUIP",
        "More information on adapting field equipment to cover cropping",
    )
    MORE_AGRONOMISTS = (
        "MORE_AGRONOMISTS",
        "More agronomist/consultant support in cover cropping",
    )
    CROP_INSURANCE = "CROP_INSURANCE", "Crop insurance breaks for cover cropping"
    OTHER = "OTHER", "Other"


class CoverCropReasonsChoices(models.TextChoices):
    """Reasons for cover cropping"""

    BLANK = "", ""
    DISEASE_PEST_MGMT = (
        "DISEASE_PEST_MGMT",
        "Beneficial insect habitat and/or disease and pest management",
    )
    CARBON = "CARBON", "Carbon sequestration"
    PROG_COST_SHARE = "PROG_COST_SHARE", "Conservation program cost sharing"
    TRAFFICABILITY = "TRAFFICABILITY", "Field trafficability"
    FORAGE = "FORAGE", "Forage production"
    WATER_QUALITY = "WATER_QUALITY", "Improve surface and/or ground water quality"
    ORGANIC_MATTER = "ORGANIC_MATTER", "Increase organic matter"
    EROSION = "EROSION", "Reduce erosion/soil erosion"
    RESILIENCE = "RESILIENCE", "Resilience of fields in extreme weather"
    SOIL_STRUCTURE = "SOIL_STRUCTURE", "Soil structure improvement"
    WEEDS = "WEEDS", "Weed suppression"
    OTHER = "OTHER", "Other reasons"


class CoverCropChoices(models.TextChoices):
    """Cover crop options"""

    BLANK = "", ""
    ANNUAL_RYEGRASS = "ANNUAL_RYEGRASS", "annual ryegrass"  # winter
    BALANSA_CLOVER = "BALANSA_CLOVER", "balansa clover"
    BARLEY = "BARLEY", "barley"  # spring
    BERSEEM_CLOVER = "BERSEEM_CLOVER", "berseem clover"  # legume
    BUCKWHEAT = "BUCKWHEAT", "buckwheat"
    CANOLA = "CANOLA", "canola/rapeseed"  # brassica
    CEREAL_RYE = "CEREAL_RYE", "cereal (winter) rye"  # winter
    CRIMSON_CLOVER = "CRIMSON_CLOVER", "crimson clover"  # legume
    COWPEA = "COWPEA", "cowpea"  # legume
    DUTCH_WHITE_CLOVER = "DUTCH_WHITE_CLOVER", "Dutch white clover"
    FIELD_PEA = "FIELD_PEA", "field/forage pea"  # legume
    FLAX = "FLAX", "flax"
    HAIRY_VETCH = "HAIRY_VETCH", "hairy vetch"  # legume
    KALE = "KALE", "kale"  # brassica
    MILLET = "MILLET", "millet"
    PLANTAIN = "PLANTAIN", "plantain"
    OATS = "OATS", "oats"  # spring
    OTHER_LEGUME = "OTHER_LEGUME", "other (legume)"  #
    OTHER_GRASS = "OTHER_GRASS", "other (grass)"  #
    OTHER_BROADLEAF = "OTHER_BROADLEAF", "other (broadleaf)"  #
    RADISH = "RADISH", "radish"  # brassica
    RED_CLOVER = "RED_CLOVER", "red clover"  # legume
    SORGHUM = "SORGHUM", "sorghum"  # grass
    SORGHUM_SUDAN = "SORGHUM_SUDAN", "sorghum-sudan"  # grass
    SOYBEANS = "SOYBEANS", "soybeans"  # legume
    SUNFLOWER = "SUNFLOWER", "sunflower"  #
    SUN_HEMP = "SUN_HEMP", "sun hemp"
    TRITICALE = "TRITICALE", "triticale"  # winter
    TURNIP = "TURNIP", "turnip"  # brassica
    WHEAT_SPRING = "WHEAT_SPRING", "wheat (spring)"  # spring
    WHEAT_WINTER = "WHEAT_WINTER", "wheat (winter)"  # winter
    WINTER_PEA = "WINTER_PEA", "winter pea"
    YELLOW_SWEET_CLOVER = "YELLOW_SWEET_CLOVER", "yellow sweet clover"
    MULTISPECIES = "MULITSPECIES", "multispecies mix of 2 or more"
    OTHER = "OTHER", "other"


class CoverCropRateUnitsChoices(models.TextChoices):
    """Choices for manure application units"""

    BLANK = "", ""
    POUNDS_ACRE = "POUNDS_ACRE", "lbs/acre"
    BUSHELS_ACRE = "BUSHELS_ACRE", "bu/acre"


class CashCropChoices(models.TextChoices):
    """Cash crops"""

    BLANK = "", ""
    CORN_FOR_GRAIN = "CORN_FOR_GRAIN", "corn for grain"
    CORN_SILAGE = "CORN_SILAGE", "corn silage"
    SOYBEANS = "SOYBEANS", "soybeans"
    WHEAT = "WHEAT", "wheat"
    OATS = "OATS", "oats"
    BARLEY = "BARLEY", "barley"
    TRITICALE = "TRITICALE", "Tritcale"
    SORGHUM = "SORGHUM", "sorghum"
    SORGHUM_SUDAN = "SORGHUM_SUDAN", "sorghum-sudan"
    ALFALFA = "ALFALFA", "alfalfa"
    VEGETABLE_CROP = "VEGETABLE_CROP", "vegetable crop"
    OTHER_GRAIN = "OTHER_GRAIN", "other grain"
    OTHER_FORAGE = "OTHER_FORAGE", "other forage"
    LIVESTOCK = "LIVESTOCK", "livestock feeding/grazing"


class SeedingMethodChoices(models.TextChoices):
    """Cover crop seeding method choices"""

    BLANK = "", ""
    FROST = "FROST", "frost seeded"
    DRILLED = "DRILLED", "drilled"
    BROADCAST_NO_INCORP = "BROADCAST_NO_INCORP", "broadcast, no incorporation"
    EARLY_INTERSEED = "EARLY_INTERSEED", "early interseeded -- broadcast"
    LATE_INTERSEED_BROADCAST = (
        "LATE_INTERSEED_BROADCAST",
        "late interseeded -- broadcast",
    )
    LATE_INTERSEED_AERIAL = "LATE_INTERSEED_AERIAL", "late interseeded -- aerial"
    BROADCAST_INCORPORATION = "BROADCAST_INCORPORATION", "broadcast + incorporation"
    FERT_BROADCAST_INCORP = (
        "FERT_BROADCAST_INCORP",
        "cover crop seed mixed with fertilizer + broadcast + incorporation",
    )
    OTHER = "OTHER", "other"


class SoilTextureClassChoices(models.TextChoices):
    """Soil texture classes"""

    BLANK = "", ""
    CLAY = "CLAY", "clay"
    CLAY_LOAM = "CLAY_LOAM", "clay loam"
    LOAM = "LOAM", "loam"
    LOAMY_SAND = "LOAMY_SAND", "loamy sand"
    SAND = "SAND", "sand"
    SANDY_CLAY = "SANDY_CLAY", "sandy clay"
    SANDY_CLAY_LOAM = "SANDY_CLAY_LOAM", "sandy clay loam"
    SANDY_LOAM = "SANDY_LOAM", "sandy loam"
    SILT = "SILT", "silt"
    SILT_LOAM = "SILT_LOAM", "silt loam"
    SILTY_CLAY = "SILTY_CLAY", "silty clay"
    SILTY_CLAY_LOAM = "SILTY_CLAY_LOAM", "silty clay loam"
    MUCK = "MUCK", "muck"
    NOT_SURE = "NOT_SURE", "not sure"


class ManureApplicateUnitsChoices(models.TextChoices):
    """Choices for manure application units"""

    BLANK = "", ""
    POUNDS_ACRE = "TONS_ACRE", "tons/acre"
    GALLONS = "GALLONS", "gallons/acre"


class TillageSystemChoices(models.TextChoices):
    """Tillage system options"""

    BLANK = "", ""
    CONVENTIONAL = "CONVENTIONAL", "conventional tillage (<15% residue)"
    REDUCED = "REDUCED", "reduced tillage (15-30% residue)"
    MULCH_TILL = (
        "MULCH_TILL",
        "conservation tillage (>30% residue) - mulch till/vertical tillage",
    )
    STRIP_TILL = "STRIP_TILL", "conservation tillage (>30% residue) - strip till"
    NO_TILL = "NO_TILL", "conservation tillage (>30% residue) - no till"


class PrimaryTillageEquipmentChoices(models.TextChoices):
    """Primary tillage equipment choices"""

    BLANK = "", ""
    MOLDBOARD = "MOLDBOARD", "moldboard plow"
    DISK_HARROW = "DISK_HARROW", "disk-harrow"
    CHISEL = "CHISEL", "chisel plow"
    DISK_CHISEL = "DISK_CHISEL", "disk-chisel"
    HIGHSPEED_DISK = "HIGHSPEED_DISK", "high-speed disk"
    NONE = "NONE", "none"
    OTHER = "OTHER", "other"


class SecondaryTillageEquipmentChoices(models.TextChoices):
    """Secondary tillage options"""

    BLANK = "", ""
    CULTIVATOR_FINISHER = "CULTIVATOR_FINISHER", "field cultivator/field finisher"
    DISK_HARROW = "DISK_HARROW", "disk-harrow"
    HIGHSPEED_DISK = "HIGHSPEED_DISK", "high-speed disk"
    VERTICAL_TILLAGE = "VERTICAL_TILLAGE", "vertical tillage"
    NONE = "NONE", "none"
    OTHER = "OTHER", "other"


class SoilConditionsSeedingChoices(models.TextChoices):
    """Soil conditions at seeding"""

    BLANK = "", ""
    DRY = "DRY", "dry"
    ADEQUATE = "ADEQUATE", "adequate moisture"
    WET = "WET", "excessively wet"


class TerminationMethodTimingChoices(models.TextChoices):
    """Termination choices"""

    BLANK = "", ""
    GRAZE_FALL = "GRAZE_FALL", "graze fall"
    WINTERKILL = "WINTERKILL", "little to no cover crop growth in spring"
    FALLKILL = "FALLKILL", "killing frost (fall)"
    GRAZE_SPRING = "GRAZE_SPRING", "graze spring"
    SPRING_HERBICIDE = (
        "SPRING_HERBICIDE",
        "early spring, herbicide application (14 plus days prior to crop establishment)",
    )
    FORAGE = "FORAGE", "harvest for forage"
    GREEN_HERBICIDE = "GREEN_HERBICIDE", "plant green, herbicide termination"
    SPRING_ROLLER_CRIMPER = (
        "SPRING_ROLLER_CRIMPER",
        "early spring, roller-crimper termination",
    )
    GREEN_ROLLER_CRIMPER = (
        "GREEN_ROLLER_CRIMPER",
        "plant green, roller-crimper termination",
    )
    OTHER = "OTHER", "other"


class Survey(models.Model):
    # Timestamp
    survey_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    notes_admin = models.TextField(
        verbose_name="Questions or comments about nutrient management and cover crops",
        null=True,
    )
    confirmed_accurate = models.BooleanField(null=True)

    # Foreign key to farmer rather than user
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, null=True)

    # Location
    farm_location = geo_models.PointField(verbose_name="Farm location", null=True)

    # 1. Years Experience
    years_experience = models.PositiveSmallIntegerField(
        verbose_name="Years experience of farming", null=True
    )

    # 2. Total acres of cover crops
    total_acres = models.IntegerField(
        verbose_name="Total acres of cover crops", null=True
    )

    # 3. Percent acres of your farm in cc?
    percent_of_farm_cc = models.PositiveSmallIntegerField(
        verbose_name="The percent of your farm, in acres, that is planted in cover crops",
        null=True,
    )
    # 4. Do you know the dominant soil series on your farm? If so, please list them below in order of how widely distributed (ex. Plano silt loam).
    dominant_soil_series_1 = models.CharField(
        verbose_name="Soil series with the greatest distribution on your farm",
        max_length=50,
        null=True,
    )
    dominant_soil_series_2 = models.CharField(
        verbose_name="Soil series with the second greatest distribution on your farm",
        max_length=50,
        null=True,
    )
    dominant_soil_series_3 = models.CharField(
        verbose_name="Soil series with the third greatest distribution on your farm",
        max_length=50,
        null=True,
    )
    dominant_soil_series_4 = models.CharField(
        verbose_name="Soil series with the fourth greatest distribution on your farm",
        max_length=50,
        null=True,
    )

    # 5. From the following list, select and rank your top 1 - 3 sources of information for nutrient management:

    info_source_nutrient_mgmt_1 = models.CharField(
        verbose_name="Top information source for nutrient management",
        choices=NutrientMgmtSourcesChoices.choices,
        max_length=30,
        null=True,
    )
    info_source_nutrient_mgmt_2 = models.CharField(
        verbose_name="Top information source for nutrient management",
        choices=NutrientMgmtSourcesChoices.choices,
        max_length=30,
        null=True,
    )
    info_source_nutrient_mgmt_3 = models.CharField(
        verbose_name="Top information source for nutrient management",
        choices=NutrientMgmtSourcesChoices.choices,
        max_length=30,
        null=True,
    )

    source_nutrient_mgmt_write_in = models.TextField(
        verbose_name="Other information source for nutrient management",
        null=True,
    )
    #
    # . For using cover crops for nutrient management, do you have any experiences to share or questions you'd like more information on?
    cov_crops_for_ntrnt_mgmt_comments_questions = models.TextField(
        verbose_name="Questions or comments about nutrient management and cover crops",
        null=True,
    )

    # 6. From the following list select and rank your top 1 - 3 most important sources of information on cover cropping:
    info_source_cover_crops_1 = models.CharField(
        verbose_name="Top information source for cover crops",
        choices=CoverCropInfoSourcesChoices.choices,
        max_length=30,
        null=True,
    )

    info_source_cover_crops_2 = models.CharField(
        verbose_name="Top information source for cover crops",
        choices=CoverCropInfoSourcesChoices.choices,
        max_length=30,
        null=True,
    )

    info_source_cover_crops_3 = models.CharField(
        verbose_name="Top information source for cover crops",
        choices=CoverCropInfoSourcesChoices.choices,
        max_length=30,
        null=True,
    )

    info_source_cover_crops_write_in = models.TextField(
        verbose_name="Other information and social media source for cover crops",
        null=True,
    )

    # 7. In terms of support for cover cropping, select and rank the top 1 to 3 factors you’d like to see more of:

    support_cover_crops_1 = models.CharField(
        verbose_name="Support for cover cropping",
        choices=CoverCropSupportChoices.choices,
        max_length=25,
        null=True,
    )

    support_cover_crops_2 = models.CharField(
        verbose_name="Support for cover cropping",
        choices=CoverCropSupportChoices.choices,
        max_length=25,
        null=True,
    )

    support_cover_crops_3 = models.CharField(
        verbose_name="Support for cover cropping",
        choices=CoverCropSupportChoices.choices,
        max_length=25,
        null=True,
    )

    support_cover_crops_write_in = models.TextField(
        verbose_name="Other support for cover crops you would like to see",
        null=True,
    )

    # 8. Are you lacking in any information regarding your selecting, planting, and managing cover crops?
    lacking_any_info_cover_crops = models.TextField(
        verbose_name="Lacking in any information regarding cover crops?",
        null=True,
    )

    # 9. If yes, what are the main barries to expansion?
    # Please share any details that will help us understand the challenges.
    barriers_to_expansion = models.TextField(
        verbose_name="What are your barriers to expansion? Please share any details to help us understand.",
        null=True,
    )

    # 10. What would it take for you to quit planting covers?
    quit_planting_cover_crops = models.TextField(
        verbose_name="What would it take for you to quit planting covers?", null=True
    )

    # 11. If so, does it influence your cover cropping decisions, and how?
    if_use_crop_insurance = models.TextField(
        verbose_name="If so, does it influence your cover cropping decisions, and how?",
        null=True,
    )
    # 12. Why do you cover crop? From the list below select and rank your top 3 - 5 motivations

    why_cover_crops_write_in = models.TextField(
        verbose_name="Other reasons you plant cover crops?",
        null=True,
    )
    # 14. Does planting a cover crop delay when you would otherwise plant your cash crop?
    cover_crops_delay_cash_crop = models.BooleanField(
        verbose_name="Does planting a cover crop delay when you would otherwise plant your cash crop?",
        null=True,
    )

    # 15a. Do you save cover crop seed?
    save_cover_crop_seed = models.BooleanField(
        verbose_name="Do you save cover crop seed?", null=True
    )
    # 15b. What is your source for cover crop seed?
    source_cover_crop_seed = models.TextField(
        verbose_name="What is your cover crop seed source?", null=True
    )

    # In the following section we ask you about your specific cover cropping practices in one field or set of fields (can be one acre ro 1,000) from which you'll take your samples for biomass, nutrient, and forage analysis. Provide answers *for that field.*
    # 16 Closest zip code for this field (so we can determine appropriate climate data and generate a location map of participating fields). Field must be located in Wisconsin.
    closest_zip_code = models.IntegerField(
        verbose_name="Enter the closest zip code for this field.", null=True
    )
    # 17 What is this field(s) acreage?
    field_acreage = models.SmallIntegerField(
        verbose_name="What is this field's acreage?", null=True
    )
    # ??	Question about multiple year rotation?
    # 18	"Please describe your crop rotation for this field including cover crops.
    # 2021. Cash crop drop down        cover crop drop down
    # 2022 Cash crop drop down        cover crop drop down
    # 2023 Cash crop drop down        cover crop drop down
    crop_rotation = models.TextField(
        verbose_name="Please describe your crop rotation for this field, including cover crops."
    )
    # 18a.
    crop_rotation_2021_cover_crop_species = models.CharField(
        verbose_name="Cover crop species in 2021",
        choices=CoverCropChoices.choices,
        max_length=30,
        null=True,
    )

    crop_rotation_2021_cash_crop_species = models.CharField(
        verbose_name="Cash crop species 2021",
        choices=CashCropChoices.choices,
        max_length=30,
        null=True,
    )
    # 18b.
    crop_rotation_2022_cover_crop_species = models.CharField(
        verbose_name="Cover crop species in 2022",
        choices=CoverCropChoices.choices,
        max_length=30,
        null=True,
    )

    crop_rotation_2022_cash_crop_species = models.CharField(
        verbose_name="Cash crop species 2022",
        choices=CashCropChoices.choices,
        max_length=30,
        null=True,
    )
    # 18c.
    crop_rotation_2023_cover_crop_species = models.CharField(
        verbose_name="Cover crop species in 2023",
        choices=CoverCropChoices.choices,
        max_length=30,
        null=True,
    )

    crop_rotation_2023_cash_crop_species = models.CharField(
        verbose_name="Cash crop species 2023",
        choices=CashCropChoices.choices,
        max_length=30,
        null=True,
    )

    # 19	"Please select any of the following that were planted as a cover crop in this field *this year*.

    # 31	At what rate did you plant your cover crops (please type species and pounds per acre).

    # Species 1
    cover_crop_species_1 = models.CharField(
        verbose_name="Cover crop species 1",
        choices=CoverCropChoices.choices,
        max_length=30,
        null=True,
    )
    cover_crop_planting_rate_1 = models.SmallIntegerField(
        verbose_name="Cover crop planting rate, for species 1", null=True
    )
    cover_crop_planting_rate_1_units = models.CharField(
        verbose_name="Units for cover crop 1 application rate",
        null=True,
        choices=CoverCropRateUnitsChoices.choices,
        max_length=15,
    )

    # Species 2
    cover_crop_species_2 = models.CharField(
        verbose_name="Cover crop species 2",
        choices=CoverCropChoices.choices,
        max_length=30,
        null=True,
    )
    cover_crop_planting_rate_2 = models.SmallIntegerField(
        verbose_name="Cover crop planting rate, for species 2", null=True
    )
    cover_crop_planting_rate_2_units = models.CharField(
        verbose_name="Units for cover crop 2 application rate",
        null=True,
        choices=CoverCropRateUnitsChoices.choices,
        max_length=15,
    )
    # Species 3
    cover_crop_species_3 = models.CharField(
        verbose_name="Cover crop species 3",
        choices=CoverCropChoices.choices,
        max_length=30,
        null=True,
    )
    cover_crop_planting_rate_3 = models.SmallIntegerField(
        verbose_name="Cover crop planting rate, for species 3", null=True
    )
    cover_crop_planting_rate_3_units = models.CharField(
        verbose_name="Units for cover crop 3 application rate",
        null=True,
        choices=CoverCropRateUnitsChoices.choices,
        max_length=15,
    )
    # Species 4
    cover_crop_species_4 = models.CharField(
        verbose_name="Cover crop species 4",
        choices=CoverCropChoices.choices,
        max_length=30,
        null=True,
    )
    cover_crop_planting_rate_4 = models.SmallIntegerField(
        verbose_name="Cover crop planting rate, for species 4", null=True
    )
    cover_crop_planting_rate_4_units = models.CharField(
        verbose_name="Units for cover crop 4 application rate",
        null=True,
        choices=CoverCropRateUnitsChoices.choices,
        max_length=15,
    )
    # Species 5
    cover_crop_species_5 = models.CharField(
        verbose_name="Cover crop species 5",
        choices=CoverCropChoices.choices,
        max_length=30,
        null=True,
    )
    cover_crop_planting_rate_5 = models.SmallIntegerField(
        verbose_name="Cover crop planting rate, for species 5", null=True
    )
    cover_crop_planting_rate_5_units = models.CharField(
        verbose_name="Units for cover crop 5 application rate",
        null=True,
        choices=CoverCropRateUnitsChoices.choices,
        max_length=15,
    )
    cover_crop_species_and_rate_write_in = models.TextField(
        verbose_name="Other cover crops planted and their rates, please specify in pounds per acre.",
        null=True,
    )

    cover_crop_multispecies_mix_write_in = models.TextField(
        verbose_name="details for multispecies mix", null=True
    )

    # 21	What date this year did you plant your cash crop in this field?
    cash_crop_planting_date = models.DateField(
        verbose_name="What date this year did you plant your cash crop in this field?",
        null=True,
    )
    # 22	How many years have you been planting cover crops *in this field*?
    years_with_cover_crops = models.SmallIntegerField(
        verbose_name="How many years have you been planting cover crops *in this field*?",
        null=True,
    )
    # 23	"Please choose the dominant soil texture of the field.
    dominant_soil_texture = models.CharField(
        verbose_name="Please select the dominant soil texture of this field.",
        choices=SoilTextureClassChoices.choices,
        max_length=15,
        null=True,
    )

    # 24	Will you apply manure prior to seeding cover crops on this field, and at what rate?
    manure_prior = models.BooleanField(
        verbose_name="Will you apply manure prior to seeding cover crops on this field?",
        null=True,
    )
    # 24a
    manure_prior_rate = models.IntegerField(
        verbose_name="At what rate will the manure be applied?", null=True
    )
    manure_prior_rate_units = models.CharField(
        verbose_name="The units for the manure application rate",
        choices=ManureApplicateUnitsChoices.choices,
        max_length=15,
        null=True,
    )

    # 25	Will manure be applied to the field after the cover crop is established?
    manure_post = models.BooleanField(
        verbose_name="Will manure be applied to the field after the cover crop is established?",
        null=True,
    )
    # 25a
    manure_post_rate = models.IntegerField(
        verbose_name="At what rate will the manure be applied?", null=True
    )
    manure_post_rate_units = models.CharField(
        verbose_name="The units for the manure application rate",
        choices=ManureApplicateUnitsChoices.choices,
        max_length=15,
        null=True,
    )
    # 26	"What is your tillage system for the cash crop preceding the cover crop?
    tillage_system_cash_crop = models.CharField(
        verbose_name="Tillage system for cash crop preceding",
        choices=TillageSystemChoices.choices,
        max_length=15,
        null=True,
    )
    # 27	"Primary tillage equipment (select all that apply) for a cash crop preceding a cover crop?
    primary_tillage_equipment = models.CharField(
        verbose_name="Primary tillage equipment",
        choices=PrimaryTillageEquipmentChoices.choices,
        max_length=30,
        null=True,
    )

    primary_tillage_equipment_write_in = models.TextField(
        verbose_name="Primary tillage equipment, write in",
        null=True,
    )
    # 28	"Secondary tillage equipment (select all that apply) for cash crop preceding the cover crop?
    secondary_tillage_equipment = models.CharField(
        verbose_name="Secondary tillage equipment",
        choices=SecondaryTillageEquipmentChoices.choices,
        max_length=30,
        null=True,
    )
    secondary_tillage_equipment_write_in = models.TextField(
        verbose_name="Secondary tillage equipment, write in",
        null=True,
    )

    # 29	"Soil conditions in this field at cover crop seeding
    soil_conditions_at_cover_crop_seeding = models.CharField(
        verbose_name="Soil conditions in this field at cover crop seeding",
        choices=SoilConditionsSeedingChoices.choices,
        max_length=10,
        null=True,
    )

    # 30	"Cover Crop Seeding Method.
    cover_crop_seeding_method = models.CharField(
        verbose_name="Cover crop seeding method",
        choices=SeedingMethodChoices.choices,
        max_length=30,
        null=True,
    )

    cover_crop_seeding_method_write_in = models.TextField(
        verbose_name="Cover crop seeding method, write in", null=True
    )

    # 32
    cover_crop_seed_cost = models.IntegerField(
        verbose_name="Estimated cover crop seed cost for this field ($/acre)", null=True
    )
    # 33	Estimated cover crop planting cost per acre in this field. Please use UW Extension Custom Rate Guide.(https://www.nass.usda.gov/Statistics_by_State/Wisconsin/Publications/WI-CRate20.pdf)
    cover_crop_planting_cost = models.IntegerField(
        verbose_name="Estimated cover crop planting cost for this field ($/acre)",
        null=True,
    )
    # 34	Cover crop planting date for this field (estimate is OK if not known).
    cover_crop_planting_date = models.DateField(
        verbose_name="Estimated cover crop planting date", null=True
    )
    # 35	"Estimated termination timing/method for this field.
    cover_crop_estimated_termination = models.CharField(
        verbose_name="Estimated termination timing/method for this field.",
        choices=TerminationMethodTimingChoices.choices,
        max_length=30,
        null=True,
    )

    # 36	Number of days estimated between crop harvest and cover crop establishment in this field.
    days_between_crop_hvst_and_cc_estd = models.SmallIntegerField(
        verbose_name="Number of days estimated between crop harvest and cover crop establishment in this field.",
        null=True,
    )
    # 37	Please share any interesting experiments, failures, equipment challenges with cover crops.
    interesting_tales = models.TextField(
        verbose_name="What has been your cover crop “learning curve”? Please share any interesting experiments including failures that have helped you adapt cover cropping to your farm.",
        null=True,
    )
    # 38	If another grower asked you where to start with cover cropping what would you recommend and why?
    where_to_start = models.TextField(
        verbose_name="Where would you tell another grower to start with cover crops? Why?",
        null=True,
    )
    # 39	Do you have any additional thoughts or questions about this data gathering process? Any important survey questions we should ask next time?
    additional_thoughts = models.TextField(
        verbose_name="Any additional thoughts or questions? Any important survey questions we should ask next time?",
        null=True,
    )

    derived_species_class = models.CharField(
        verbose_name="Cover crop species class",
        max_length=90,
        null=True,
    )

    derived_county = models.CharField(max_length=250, blank=True)

    def derive_species_class(self):
        self.derived_species_class = derive_species_class(self)

    def populate_county(self):
        """Populate a usuable county name
        - first check to see if we can use farm_location
        - then use provided zipcode: use 5 digit to centroid table?
        - if all outside wisc? not used
        """
        id = self.id

        def lookup_county_from_loc(id):
            from django.db import connection

            with connection.cursor() as cursor:
                cursor.execute(
                    f"""
                select wc.countyname 
                from wisccc_survey ws
                left join wi_counties wc
                on ST_Intersects(ws.farm_location, wc.shape)
                where ws.id = {id}"""
                )
                row = cursor.fetchone()

            derived_county = row[0]
            return derived_county

        if self.farm_location is not None:
            self.derived_county = lookup_county_from_loc(id)
        else:
            self.derived_county = ""

    # open_to_sharing = models.BooleanField(
    #     verbose_name="(Would you be open to having your cover cropping experience shared on our website for other interested farmers?)",
    #     null=True,
    # )
    class Meta:
        permissions = (("survery_manager", "Survey Manager"),)


class SurveyPhoto(models.Model):

    survey_response = models.ForeignKey(Survey, on_delete=models.CASCADE, null=True)
    uploaded_time = models.DateTimeField(auto_now_add=True)
    image_1 = models.ImageField(storage=WiscCCPhotoStorage(), null=True)
    caption_photo_1 = models.CharField(
        max_length=50, verbose_name="Caption about photo 1", null=True
    )
    image_2 = models.ImageField(storage=WiscCCPhotoStorage(), null=True)
    caption_photo_2 = models.CharField(
        max_length=50, verbose_name="Caption about photo 2", null=True
    )
    notes = models.TextField(verbose_name="Notes about photo", null=True)


class SurveyRegistration(models.Model):
    """For folks registering to take survey"""

    class BiomassOrJustSurveyChoices(models.TextChoices):
        BIOMASS_AND_SURVEY = (
            "BIOMASS_AND_SURVEY",
            "I am willing to collect fall and spring cover crop samples from one of my fields, and complete a fall survey on cover crop practices ($100 honorarium plus biomass and nutrient quality analysis of samples).",
        )
        JUST_SURVEY = (
            "JUST_SURVEY",
            "I can share my cover cropping experiences in a survey ($25 honorarium) but prefer not to sample my fields.",
        )

    class HaveAKit(models.TextChoices):
        HAVE_A_KIT = (
            "HAVE_A_KIT",
            "I have a biomass sampling kit from previous years’ participation. You will send me reminder instructions & prepaid addressed envelopes for my 2024-5 samples.",
        )
        NEED_A_KIT = (
            "NEED_A_KIT",
            "I need a biomass sampling kit sent to the address above along with instructions & prepaid addressed envelopes for my 2024-5 samples.",
        )

    survey_year = models.IntegerField(null=True)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, null=True)
    signup_timestamp = models.DateTimeField(auto_now_add=True)
    belong_to_groups = models.TextField(
        verbose_name="Do you belong to producer led watershed groups?", null=True
    )
    howd_you_hear = models.TextField(
        verbose_name="How'd you hear about this project?", null=True
    )
    notes = models.TextField(null=True)
    biomass_or_just_survey = models.CharField(
        verbose_name="Biomass and survey or just survey",
        null=True,
        max_length=20,
        choices=BiomassOrJustSurveyChoices.choices,
    )
    do_you_have_a_biomas_kit = models.CharField(
        verbose_name="Do you have a biomass sampling kit from previous years?",
        choices=HaveAKit.choices,
        max_length=250,
        null=True,
    )
    do_you_need_assistance = models.TextField(
        verbose_name="I need some assistance",
        null=True,
    )
