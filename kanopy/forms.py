from django import forms
from django.contrib.gis import forms
from kanopy.models import Groundcoverdoc, Samplepoint
# from leaflet.forms.widgets import LeafletWidget
# from leaflet.forms.fields import PointField

class GroundcoverForm(forms.ModelForm):

    description = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control form-control-lg",
                }
            ),
        )
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
        fields = ('locname', 'description', 'image', 'collectionpoint')


class AddPointForm(forms.ModelForm):
    description = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control form-control-lg",
                }
            ),
        )
    sampleloc = forms.PointField(
        widget=forms.OpenLayersWidget(
            attrs={
                'map_width': 800,
                'map_height': 500,
                }
            ),
        )

    class Meta:
        model = Samplepoint
        fields = ['description', 'sampleloc']