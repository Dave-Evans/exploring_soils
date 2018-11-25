from django import forms
from .models import Study, Rep

class NewStudyForm(forms.ModelForm):
    # message = forms.CharField(
    #     widget=forms.Textarea(
    #         attrs={'rows': 5, 'placeholder': 'What is on your mind?'}
    #     ),
    #     max_length=4000,
    #     help_text='The max length of the text is 4000.'
    # )
    class Meta:
        model = Study
        fields = ['name', 'description',\
            'plot_cnt_wide', 'plot_cnt_long',\
            'plot_sz_wide', 'plot_sz_long',\
            'alley_dist_wide', 'alley_dist_long',\
            'metric']

class NewRepForm(forms.ModelForm):

    class Meta:
        model = Rep

        fields = [
            'study',
            'block',
            'rep_name',
            'lower_left_corner_y',
            'lower_left_corner_x',
            'upper_left_corner_y',
            'upper_left_corner_x'
        ]