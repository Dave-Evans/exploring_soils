from django import forms
from kanopy.models import Groundcoverdoc

class GroundcoverForm(forms.ModelForm):
    class Meta:
        model = Groundcoverdoc
        fields = ('locname', 'description', 'image', 'latitude', 'longitude')

