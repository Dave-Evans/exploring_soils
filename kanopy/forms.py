from django import forms
from django.contrib.gis import forms as geo_forms
from kanopy.models import Groundcoverdoc, CoverCrops, SeedingMethod, CashCrops
# from leaflet.forms.widgets import LeafletWidget
# from leaflet.forms.fields import PointField

class GroundcoverForm(forms.ModelForm):


    locname = forms.CharField(label = 'Location name', help_text='to differentiate multiple photos from the same field')
    
    # Only one is required
    cover_crop_species_1 = forms.ChoiceField(label = 'Cover crop species', choices = CoverCrops.choices, required=True)
    cover_crop_species_2 = forms.ChoiceField(label = 'Additional cover crop species', choices = CoverCrops.choices, required=False, initial = '')
    cover_crop_species_3 = forms.ChoiceField(label = "Add'l cover crop species", choices = CoverCrops.choices, required=False, initial = '')
    cover_crop_species_4 = forms.ChoiceField(label = "Add'l cover crop species", choices = CoverCrops.choices, required=False, initial = '')
    
    comments = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control form-control-lg",
                }
            ),
         required=False
        )
     
    fgcc_value = forms.DecimalField(
        widget = forms.TextInput(attrs={'readonly':'readonly'}),
        label ='Fractional Green Canopy Cover',
        required=False
    )

    collectionpoint = geo_forms.PointField(
        # widget=forms.OpenLayersWidget(
            # attrs={
                # 'map_width': 800,
                # 'map_height': 500,
                # 'default_lat' : 44.6720744,
                # 'default_lon' : -93.1725846,
                # 'default_zoom': 7
                # }
            # ),
        # )
        label="Location",
        help_text='Click on the map in the location where the photo was taken',
        widget=geo_forms.OSMWidget(
            attrs={
                # 'map_width': 650,
                # 'map_height': 500,
                'default_lat' : 44.6720744,
                'default_lon' : -93.1725846,
                'default_zoom': 7
                }
            ),
        )

    class Meta:
        model = Groundcoverdoc
        fields = (
            'locname', 
            'cover_crop_species_1',
            'cover_crop_species_2',
            'cover_crop_species_3',
            'cover_crop_species_4',
            'cover_crop_planting_date',
            'cover_crop_planting_rate',
            'crop_prior',
            'seeding_method',
            'cover_crop_termination_date',
            'image',
            'collectionpoint',
            'fgcc_value',
            'comments'
        )

