from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from bikemileage.models import Mileage


class MileageForm(forms.ModelForm):

    # ride_date = forms.DateField(input_formats=['%Y-%m-%d'], widget=XDSoftDatePickerInput()) 
    # ride_date = forms.DateField(widget=forms.SelectDateWidget()) 
    ride_date = forms.DateField(input_formats=['%Y-%m-%d']) 

    class Meta:
        
        model = Mileage
        fields = ('ride_date', 'rider', 'mileage', 'bike_type', 'comment', 'cost')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save ride'))
