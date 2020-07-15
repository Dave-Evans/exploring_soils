from django import forms
from django.contrib.gis import forms
from kanopy.models import Groundcoverdoc
# from leaflet.forms.widgets import LeafletWidget
# from leaflet.forms.fields import PointField

class GroundcoverForm(forms.ModelForm):


    locname = forms.CharField(label = 'Location name')
    comments = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control form-control-lg",
                }
            ),
        )
     
    fgcc_value = forms.DecimalField(widget = forms.TextInput(attrs={'readonly':'readonly'}), label ='Fractional Green Canopy Cover')

    collectionpoint = forms.PointField(
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
        widget=forms.OSMWidget(
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

