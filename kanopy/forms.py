from django import forms
from django.contrib.gis import forms
from kanopy.models import Groundcoverdoc, Samplepoint
# from leaflet.forms.widgets import LeafletWidget
# from leaflet.forms.fields import PointField

class GroundcoverForm(forms.ModelForm):
    class Meta:
        model = Groundcoverdoc
        fields = ('locname', 'description', 'image', 'latitude', 'longitude', 'collectionpoint')

# class SamplepointForm(forms.ModelForm):

# sampleloc = PointField()

# class Meta:
# model = Samplepoint 
# fields = ('description', 'sampleloc')
# widgets = {'geom': LeafletWidget()}

#description = floppy_forms.CharField()
#sampleloc = floppy_forms.gis.PointField()

# class Meta:
#   model = SamplePoint
#   fields = ('description', 'sampleloc')






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