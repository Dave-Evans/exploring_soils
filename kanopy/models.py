from django.db import models
from djgeojson.fields import PointField
from django.contrib.gis.db import models as geo_models

class CoverCrops(models.TextChoices):
    '''Different Cover crops from which to choose'''
    NONE = None, '----------'
    ALFALFA = 'ALFALFA', 'Alfalfa (Medicago sativa)'
    ANNUAL_RYE = 'ANNUAL_RYE', 'Annual Rye (Lolium multiflorum'
    BUCKWHEAT = 'BUCKWHEAT', 'Buckweat (Fagopyrum esculentum)'
    CAMELINA = 'CAMELINA', 'Camelina (Camelina sativa)'
    CEREAL_RYE = 'CEREAL_RYE', 'Cereal Rye (Secale cereale)'
    COWPEAS = 'COWPEAS', 'Cowpeas (Vigna unguiculata)'
    CRIMSON_CLOVER = 'CRIMSON_CLOVER', 'Crimson Clover (Trifolium incarnatum)'
    HAIRY_VETCH = 'HAIRY_VETCH', 'Hairy Vetch (Vicia villosa)'
    MUSTARDS = 'MUSTARDS', 'Mustartds (Brassicaceae)'
    OATS = 'OATS', 'Oats (Avena sativa)'
    PENNYCRESS = 'PENNYCRESS', 'Pennycress (Thlaspi arvense)'
    RADISH = 'RADISH', 'Radish (Raphanus sativus)'
    RAPESEED = 'RAPESEED', 'Rapeseed (Brassica napus)'
    RED_CLOVER = 'RED_CLOVER', 'Red Clover (Trifolium pratense)'
    SUNN_HEMP = 'SUNN_HEMP', 'Sunn Hemp (Crotalaria juncea)'
    TURNIP = 'TURNIP', 'Turnip (Brassica rapa var. rapa)'
    WHITE_CLOVER = 'WHITE_CLOVER', 'White Clover (Trifolium repens)'
    OTHER = 'OTHER', 'Other'
    
    
class SeedingMethod(models.TextChoices):
    '''Different seeding methods'''
    DRILL = 'DRILL', 'Drill'
    BROADCAST = 'BROADCAST', 'Broadcast'
    BROADCAST_INCORPORATION = 'BROADCAST_INCORPORATION', 'Broadcast plus incorporation'
    AERIAL = 'AERIAL', 'Aerial'
    MANURE_SLURRY = 'MANURE_SLURRY', 'Manure slurry'
    OTHER = 'OTHER', 'Other'
    
class CashCrops(models.TextChoices):
   '''Different cash crops'''
   CORN = 'CORN', 'Corn'
   CORN_SILAGE = 'CORN_SILAGE', 'Corn silage'
   SOY_BEANS = 'SOY_BEANS', 'Soy beans'
   SMALL_GRAIN = 'SMALL_GRAIN', 'Small grain'
   CANNING_CROP = 'CANNING_CROP', 'Canning crop'
   POTATOES = 'POTATOES', 'Potatoes'
   DRY_BEANS = 'DRY_BEANS', 'Dry beans'
   SUGAR_BEETS = 'SUGAR_BEETS', 'Sugar beets'
   PREVENT_PLANT = 'PREVENT_PLANT', 'Prevent plant'
   OTHER = 'OTHER', 'Other'
   

class Groundcoverdoc(models.Model):
    
    collectionpoint = geo_models.PointField(verbose_name="Collection Point", null=True)
    
    image = models.ImageField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    fgcc_value = models.DecimalField(max_digits=10, decimal_places=7, blank=True)
    
    cover_crop_species_1 = models.CharField(
        max_length=25, 
        choices=CoverCrops.choices
    )
    
    cover_crop_species_2 = models.CharField(
        max_length=25, 
        choices=CoverCrops.choices,
        blank=True
    )
    cover_crop_species_3 = models.CharField(
        max_length=25, 
        choices=CoverCrops.choices,
        blank=True
    )
    cover_crop_species_4 = models.CharField(
        max_length=25, 
        choices=CoverCrops.choices,
        blank=True
    )
    
    cover_crop_planting_date = models.DateField()
    
    cover_crop_termination_date = models.DateField(blank=True)
    
    cover_crop_planting_rate = models.FloatField(help_text = 'in pounds per acre')
    
    crop_prior = models.CharField(
        max_length=25,
        choices=CashCrops.choices
    ) 

    seeding_method = models.CharField(
        max_length=55,
        choices=SeedingMethod.choices
    )
    
    comments = models.TextField(blank=True)

    contact_email = models.EmailField(blank=True)
