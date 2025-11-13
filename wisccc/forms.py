from django import forms
from django.contrib.gis import forms as geo_forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UsernameField,
)

from accounts.forms import TurnstileField
from wisccc.models import (
    SurveyFarm,
    SurveyField,
    FieldFarm,
    Farmer,
    SurveyPhoto,
    SurveyRegistration,
    Researcher,
    AncillaryData,
    InterestedParty,
    InterestedAgronomist,
)
from wisccc.models import (
    CashCropChoices,
    CoverCropChoices,
    CoverCropChoicesWMulti,
    CoverCropInfoSourcesChoices,
    CoverCropSupportChoices,
    CoverCropReasonsChoices,
    ExpandAcresChoices,
    HowSatisfiedChoices,
    ManureApplicateUnitsChoices,
    ManureSourceChoices,
    ManureConsistencyChoices,
    NutrientMgmtSourcesChoices,
    PrimaryTillageEquipmentChoices,
    SecondaryTillageEquipmentChoices,
    SeedingMethodChoices,
    SoilConditionsSeedingChoices,
    SoilTextureClassChoices,
    TerminationMethodTimingChoices,
    TillageSystemChoices,
    TopGoalChoices,
    CoverCropRateUnitsChoices,
    StateAbrevChoices,
)

TRUE_FALSE_CHOICES = (("", ""), (True, "Yes"), (False, "No"))
TRUE_FALSE_CHOICES_SHARE_OR_ANON = (
    ("", ""),
    (True, "Yes, you can attribute the above quote to me."),
    (False, "No, I prefer to remain anonymous.")
    )


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "", "id": "hello"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "id": "hi",
            }
        )
    )


class FarmerForm(forms.ModelForm):
    first_name = forms.CharField(max_length=250, required=True)
    last_name = forms.CharField(max_length=250, required=True)
    phone_number = forms.CharField(max_length=13, required=True)
    address_street = forms.CharField(
        label="Street Address", max_length=250, required=True
    )
    address_municipality = forms.CharField(
        label="Municipality", max_length=250, required=True
    )
    address_state = forms.ChoiceField(
        label="State",
        choices=StateAbrevChoices.choices,
        required=True,
    )
    address_zipcode = forms.IntegerField(label="Zip code", required=True)
    farm_name = forms.CharField(max_length=250, required=False)
    county = forms.CharField(
        max_length=500,
        label="In what county do you farm? (If you farm in more than one, list them in order of number of acres.) ",
        required=True,
        widget=forms.Textarea(attrs={"rows": 5}),
    )

    class Meta:
        model = Farmer
        fields = (
            "first_name",
            "last_name",
            "phone_number",
            "farm_name",
            "county",
            "address_street",
            "address_municipality",
            "address_zipcode",
        )


class SurveyFarmFormFull(forms.ModelForm):

    # 1. Total acres of cover crops
    total_acres = forms.IntegerField(
        label="1. Total acres you planted to cover crops this year.",
        required=True,
        min_value=0,
        max_value=100000,
    )

    # 3. Percent acres of your farm in cc?
    percent_of_farm_cc = forms.IntegerField(
        label="2. What percent of all your farm acres did you plant to covers this year?",
        required=True,
        min_value=0,
        max_value=100,
    )

    # 2. Years Experience
    years_experience = forms.IntegerField(
        label="3. How many years' of experience do you have planting cover crops?",
        required=True,
        min_value=0,
        max_value=100,
    )

    # Modified to scenario choices 2025
    main_cc_goal_this_year = forms.ChoiceField(
        label="4. For the field you plan to sample a cover crop from, please select the top goal for why you are growing cover this year.",
        choices=TopGoalChoices.choices,
        required=True,
        initial=TopGoalChoices.BLANK,
    )

    main_cc_goal_this_year_write_in = forms.CharField(
        label="4a. If you selected 'other', please describe your top goal. Please also share any other goals or thoughts on why you are growing cover crops this year.",
        required=False,
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=1000,
    )

    satisfied_with_cc_results = forms.CharField(
        label="How satisfied are you with the results you get from cover cropping? ",
        required=False,
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=500,
    )

    # 4. Do you know the dominant soil series on your farm? If so, please list them below in order of how widely distributed (ex. Plano silt loam).
    dominant_soil_series_1 = forms.CharField(
        label="4. If you know the dominant soil series on your farm please list them below in order of how widely distributed. (ex. Plano, Drummer, Tama).",
        help_text="Most dominant",
        max_length=50,
        required=True,
    )
    # 4b
    dominant_soil_series_2 = forms.CharField(
        label="",
        help_text="Second most dominant",
        max_length=50,
        required=False,
    )
    # 4c
    dominant_soil_series_3 = forms.CharField(
        label="",
        help_text="Third most dominant",
        max_length=50,
        required=False,
    )
    # 4d
    dominant_soil_series_4 = forms.CharField(
        label="",
        help_text="Fourth most dominant",
        max_length=50,
        required=False,
    )

    # 5a. From the following list, select and rank your top 1 - 3 sources of information for nutrient management:
    info_source_nutrient_mgmt_1 = forms.ChoiceField(
        label="5. What are your top three sources of information for nutrient management?",
        help_text="First",
        choices=NutrientMgmtSourcesChoices.choices,
        required=True,
    )
    # 5b.
    info_source_nutrient_mgmt_2 = forms.ChoiceField(
        label="",
        help_text="Second",
        choices=NutrientMgmtSourcesChoices.choices,
        required=True,
    )
    # 5c.
    info_source_nutrient_mgmt_3 = forms.ChoiceField(
        label="",
        help_text="Third",
        choices=NutrientMgmtSourcesChoices.choices,
        required=True,
    )

    source_nutrient_mgmt_write_in = forms.CharField(
        label='6. If you chose "other" please explain.',
        required=False,
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=500,
    )
    # 7. For using cover crops for nutrient management, do you have any experiences to share or questions you'd like more information on?
    cov_crops_for_ntrnt_mgmt_comments_questions = forms.CharField(
        label="7. Please share any experiences or questions regarding using cover crops for nutrient management.",
        required=False,
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=1000,
    )

    # 8. From the following list select and rank your top 1 - 3 most important sources of information on cover cropping:
    info_source_cover_crops_1 = forms.CharField(
        label="8. What are your top sources of outside information on cover cropping in order of importance?",
        help_text="Answers might include Agronomist, CCA, or other private consultant, friends and neighbor farmers, local cooperative, land conservation office, producer-led Watershed Group, UW Extension",
        required=False,
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=500,
    )

    info_source_cover_crops_2 = forms.ChoiceField(
        label="Not used for 2024",
        help_text="Second",
        choices=CoverCropInfoSourcesChoices.choices,
        required=False,
    )

    info_source_cover_crops_3 = forms.ChoiceField(
        label="Not used for 2024",
        help_text="Third",
        choices=CoverCropInfoSourcesChoices.choices,
        required=True,
    )
    # 9
    info_source_cover_crops_write_in = forms.CharField(
        label='9. If you chose "social media" or "other" please provide details.',
        required=False,
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=500,
    )

    biggest_challenge_cc = forms.CharField(
        label="What is your biggest challenge or unanswered question when it comes to cover cropping?",
        required=True,
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=500,
    )

    learning_history_cc = forms.CharField(
        label="How would you describe your learning history for cover cropping (including personal experience)?",
        required=True,
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=500,
    )

    conservation_programs = forms.CharField(
        label="Are you enrolled, or have you recently enrolled in Federal conservation programs such as EQIP, or CSP, or state or county programs that support your conservation practices? Which ones?",
        required=False,
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=500,
    )

    # 10. In terms of support for cover cropping, select and rank the top 1 to 3 factors you’d like to see more of:
    support_cover_crops_1 = forms.ChoiceField(
        label="10. Which of the following would make the biggest difference to you in terms of support for using cover crops?",
        choices=CoverCropSupportChoices.choices,
        required=True,
    )
    # 11
    support_cover_crops_write_in = forms.CharField(
        label="11. If you chose “other” please provide details.",
        required=False,
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=500,
    )

    # 12. Are you lacking in any information regarding your selecting, planting, and managing cover crops?
    lacking_any_info_cover_crops = forms.CharField(
        label="12. Are you lacking in any information regarding cover crops? Please explain.",
        required=True,
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=500,
    )

    barriers_to_expansion = forms.ChoiceField(
        label="13. Would you like to expand the number of acres you cover crop?",
        required=True,
        choices=ExpandAcresChoices.choices,
    )

    barriers_to_expansion_write_in = forms.CharField(
        label="If you chose “other” please provide details.",
        required=False,
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=1000,
    )

    quit_planting_cover_crops = forms.CharField(
        label="14. What would it take for you to quit planting covers?",
        required=True,
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=500,
    )

    if_use_crop_insurance = forms.CharField(
        label="15. Do you use crop insurance? If so, does it influence your cover cropping decisions, and how?",
        required=True,
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=500,
    )
    why_cover_crops_write_in = forms.CharField(
        label="16. What are your top 3 motivations for cover cropping? Please explain.",
        help_text="Answers might include nutrient management, disease and pest management, carbon sequestration, conservation program cost sharing, forage production, water quality, build organic matter, soil erosion, resilience/trafficability of fields, soil structure, weed suppression, it's the right thing to do, etc.",
        required=True,
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=500,
    )
    # 34. Does planting a cover crop delay when you would otherwise plant your cash crop?
    cover_crops_delay_cash_crop = forms.ChoiceField(
        label="34. Does planting a cover crop delay when you would otherwise plant your cash crop?",
        choices=TRUE_FALSE_CHOICES,
        required=True,
    )

    # 35. Do you save cover crop seed?
    save_cover_crop_seed = forms.ChoiceField(
        label="35. Do you save cover crop seed?",
        required=True,
        choices=TRUE_FALSE_CHOICES,
    )
    # 36. What is your source for cover crop seed?
    source_cover_crop_seed = forms.CharField(
        label="36. What is your cover crop seed source?",
        required=True,
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=500,
    )
    # 49	Please share any interesting experiments, failures, equipment challenges with cover crops.
    interesting_tales = forms.CharField(
        label="49. What's been your cover crop learning curve? Share any interesting experiments or failures.",
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=1000,
        required=True,
    )
    # 50	If another grower asked you where to start with cover cropping what would you recommend and why?
    where_to_start = forms.CharField(
        label="50. Where would you tell another grower to start with cover crops? Why?",
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=1000,
        required=True,
    )
    # 51	Do you have any additional thoughts or questions about this data gathering process? Any important survey questions we should ask next time?
    additional_thoughts = forms.CharField(
        label="51. Any additional thoughts or questions? Any important survey questions we should ask next time?",
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=1000,
        required=False,
    )

    encourage_cc = forms.ChoiceField(
        label="Which of the following would do the most to encourage more farmers to cover crop?",
        choices=CoverCropSupportChoices.choices,
        required=False,
    )

    encourage_cc_write_in = forms.CharField(
        label="Please explain.",
        widget=forms.Textarea(attrs={"rows": 5}),
        required=False,
    )

    notes_admin = forms.CharField(
        label="Notes about survey response (for admin purposes)",
        widget=forms.Textarea,
        max_length=5000,
        required=False,
    )

    confirmed_accurate = forms.ChoiceField(
        label="Is all the information in this entry accurate?",
        required=False,
        choices=TRUE_FALSE_CHOICES,
    )

    class Meta:
        model = SurveyFarm
        fields = (
            "years_experience",
            "total_acres",
            "percent_of_farm_cc",
            "main_cc_goal_this_year",
            "main_cc_goal_this_year_write_in",
            "satisfied_with_cc_results",
            "dominant_soil_series_1",
            "dominant_soil_series_2",
            "dominant_soil_series_3",
            "dominant_soil_series_4",
            "info_source_nutrient_mgmt_1",
            "info_source_nutrient_mgmt_2",
            "info_source_nutrient_mgmt_3",
            "source_nutrient_mgmt_write_in",
            "cov_crops_for_ntrnt_mgmt_comments_questions",
            "info_source_cover_crops_1",
            "info_source_cover_crops_2",
            "info_source_cover_crops_3",
            "info_source_cover_crops_write_in",
            "biggest_challenge_cc",
            "learning_history_cc",
            "conservation_programs",
            "support_cover_crops_1",
            "support_cover_crops_write_in",
            "lacking_any_info_cover_crops",
            "barriers_to_expansion",
            "barriers_to_expansion_write_in",
            "quit_planting_cover_crops",
            "if_use_crop_insurance",
            "why_cover_crops_write_in",
            "cover_crops_delay_cash_crop",
            "save_cover_crop_seed",
            "source_cover_crop_seed",
            "interesting_tales",
            "where_to_start",
            "additional_thoughts",
            "encourage_cc",
            "encourage_cc_write_in",
            "confirmed_accurate",
            "notes_admin",
        )


class FieldFarmFormFull(forms.ModelForm):
    """For static data about a farmer's field"""

    field_name = forms.CharField(
        label="Please enter a name for this field", required=False, max_length=250
    )
    # 16 Closest zip code for this field (so we can determine appropriate climate data and generate a location map of participating fields). Field must be located in Wisconsin.
    closest_zip_code = forms.IntegerField(
        label="17. Enter the closest zip code for this field.",
        required=True,
        min_value=0,
        max_value=99999,
    )
    # 18 What is this field(s) acreage?
    field_acreage = forms.IntegerField(
        label="18. What is this field's acreage?", required=True, min_value=0
    )
    # 19 In the following section we ask you about your specific cover cropping practices in one field or set of fields (can be one acre ro 1,000) from which you'll take your samples for biomass, nutrient, and forage analysis. Provide answers *for that field.*
    field_location = geo_forms.PointField(
        label="19. Zoom in to the map and click the general location for this field.",
        help_text="To reset the location, click 'Delete all features' and click a different location",
        widget=geo_forms.OSMWidget(
            attrs={
                "default_lat": 44.636774,
                "default_lon": -90.012530,
                "default_zoom": 6,
            }
        ),
        required=False,
    )

    class Meta:
        model = FieldFarm
        fields = (
            "field_name",
            "closest_zip_code",
            "field_acreage",
            "field_location",
        )


class SurveyFieldFormFull(forms.ModelForm):

    crop_rotation_2021_cash_crop_species = forms.ChoiceField(
        label="15a. Cash crop planted 2022",
        choices=CashCropChoices.choices,
        required=True,
        initial=CashCropChoices.BLANK,
    )

    crop_rotation_2021_cover_crop_species = forms.ChoiceField(
        label="15b. Cover crop planted 2022",
        choices=CoverCropChoicesWMulti.choices,
        required=True,
        initial=CoverCropChoices.BLANK,
    )

    # 21 a.
    crop_rotation_2022_cash_crop_species = forms.ChoiceField(
        label="16a. Cash crop planted 2023",
        choices=CashCropChoices.choices,
        required=True,
    )
    # 21 b
    crop_rotation_2022_cover_crop_species = forms.ChoiceField(
        label="16b. Cover crop planted 2023",
        choices=CoverCropChoicesWMulti.choices,
        required=True,
        initial=CoverCropChoices.BLANK,
    )
    # 22 a.
    crop_rotation_2023_cash_crop_species = forms.ChoiceField(
        label="17a. Cash crop planted 2024",
        choices=CashCropChoices.choices,
        required=True,
    )
    # 22 b.
    crop_rotation_2023_cover_crop_species = forms.ChoiceField(
        label="17b. Cover crop planted 2024",
        choices=CoverCropChoicesWMulti.choices,
        required=True,
    )

    # Question 18, labeled as such in the form_ html
    # Species 1
    cover_crop_species_1 = forms.ChoiceField(
        label="a. Species",
        choices=CoverCropChoices.choices,
        required=True,
    )
    # 24b
    cover_crop_planting_rate_1 = forms.IntegerField(
        label="b. Planting rate", required=True
    )
    # 24c
    cover_crop_planting_rate_1_units = forms.ChoiceField(
        label="c. Planting rate units",
        choices=CoverCropRateUnitsChoices.choices,
        required=True,
    )
    # Species 2
    # 25a
    cover_crop_species_2 = forms.ChoiceField(
        label="d. Species",
        choices=CoverCropChoices.choices,
        required=False,
    )
    # 25b
    cover_crop_planting_rate_2 = forms.IntegerField(
        label="e. Planting rate", required=False
    )
    # 25c
    cover_crop_planting_rate_2_units = forms.ChoiceField(
        label="f. Planting rate units",
        choices=CoverCropRateUnitsChoices.choices,
        required=False,
    )
    # Species 3
    # 26
    cover_crop_species_3 = forms.ChoiceField(
        label="g. Species",
        choices=CoverCropChoices.choices,
        required=False,
    )
    cover_crop_planting_rate_3 = forms.IntegerField(
        label="h. Planting rate", required=False
    )
    cover_crop_planting_rate_3_units = forms.ChoiceField(
        label="i. Planting rate units",
        choices=CoverCropRateUnitsChoices.choices,
        required=False,
    )
    # Species 4
    # 27
    cover_crop_species_4 = forms.ChoiceField(
        label="j. Species",
        choices=CoverCropChoices.choices,
        required=False,
    )
    cover_crop_planting_rate_4 = forms.IntegerField(
        label="k. Planting rate", required=False
    )
    cover_crop_planting_rate_4_units = forms.ChoiceField(
        label="l. Planting rate units",
        choices=CoverCropRateUnitsChoices.choices,
        required=False,
    )
    # Species 5
    # 28
    cover_crop_species_5 = forms.ChoiceField(
        label="m. Species",
        choices=CoverCropChoices.choices,
        required=False,
    )
    cover_crop_planting_rate_5 = forms.IntegerField(
        label="n. Planting rate", required=False
    )
    cover_crop_planting_rate_5_units = forms.ChoiceField(
        label="o. Planting rate units",
        choices=CoverCropRateUnitsChoices.choices,
        required=False,
    )
    # 23	"Please describe your crop rotation for this field including cover crops.
    crop_rotation = forms.CharField(
        label="19. Are there any other details about your crop rotation or cover crop planting rates you'd like to share?",
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=500,
        required=False,
    )

    # # 29
    # cover_crop_species_and_rate_write_in = forms.CharField(
    #     label="29. Other cover crops planted and their rates, please specify in pounds per acre.",
    #     widget=forms.Textarea(attrs={"rows": 5}),
    #     max_length=500,
    #     required=False,
    # )
    # 30
    # cover_crop_multispecies_mix_write_in = forms.CharField(
    #     label="30. If you planted a multispecies mix in 2023 please provide details.",
    #     widget=forms.Textarea(attrs={"rows": 5}),
    #     max_length=500,
    #     required=False,
    # )

    # 31	What date this year did you plant your cash crop in this field?
    cash_crop_planting_date = forms.DateField(
        label="31. What date did you plant your cash crop in this field? (Approximate date is fine if you aren't sure.)",
        required=True,
    )
    # 32	How many years have you been planting cover crops *in this field*?
    # years_with_cover_crops = forms.IntegerField(
    #     label="32. How many years have you been planting cover crops *in this field*?",
    #     required=True,
    #     min_value=0,
    #     max_value=100,
    # )
    # 46	Cover crop planting date for this field (estimate is OK if not known).
    cover_crop_planting_date = forms.DateField(
        label="22. Cover crop planting date for this field (estimate is OK if not known).",
        required=True,
    )
    # 47	"Estimated termination timing/method for this field.
    cover_crop_estimated_termination = forms.ChoiceField(
        label="23a. Estimated termination timing/method for this field.",
        choices=TerminationMethodTimingChoices.choices,
        required=True,
    )
    cover_crop_estimated_termination_write_in = forms.CharField(
        label="23b. Please explain if you selected other.",
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=500,
        required=False,
    )
    # 48	Number of days estimated between crop harvest and cover crop establishment in this field.
    days_between_crop_hvst_and_cc_estd = forms.IntegerField(
        label="24. Number of days estimated between crop harvest and cover crop establishment in this field.",
        min_value=0,
        max_value=365,
        required=True,
    )
    # 33	"Please choose the dominant soil texture of the field.
    dominant_soil_texture = forms.ChoiceField(
        label="30. Please select the dominant soil texture of this field.",
        choices=SoilTextureClassChoices.choices,
        required=True,
    )

    # 37a	Will you apply manure prior to seeding cover crops on this field, and at what rate?
    manure_prior = forms.ChoiceField(
        label="25a. Will you apply manure prior to seeding cover crops on this field?",
        required=True,
        choices=TRUE_FALSE_CHOICES,
    )
    # 37b
    manure_prior_rate = forms.IntegerField(
        label="25b. At what rate will the manure be applied?",
        required=False,
        min_value=0,
    )
    # 37c
    manure_prior_rate_units = forms.ChoiceField(
        label="25c. Please select the units for the manure application rate.",
        choices=ManureApplicateUnitsChoices.choices,
        required=False,
    )

    # 38a Will manure be applied to the field after the cover crop is established?
    manure_post = forms.ChoiceField(
        label="26a. Will manure be applied to the field after the cover crop is established?",
        required=True,
        choices=TRUE_FALSE_CHOICES,
    )
    # 38b
    manure_post_rate = forms.IntegerField(
        label="26b. At what rate will the manure be applied?",
        required=False,
        min_value=0,
    )
    # 38c
    manure_post_rate_units = forms.ChoiceField(
        label="26c. The units for the manure application rate",
        choices=ManureApplicateUnitsChoices.choices,
        required=False,
    )
    # 39	"What is your tillage system for the cash crop preceding the cover crop?
    tillage_system_cash_crop = forms.ChoiceField(
        label="27. What is your tillage system for the cash crop preceding the cover crop?",
        choices=TillageSystemChoices.choices,
        required=True,
    )
    # 40a	"Primary tillage equipment (select all that apply) for a cash crop preceding a cover crop?
    primary_tillage_equipment = forms.ChoiceField(
        label="28a. Primary tillage equipment (select all that apply) for a cash crop preceding a cover crop?",
        choices=PrimaryTillageEquipmentChoices.choices,
        required=True,
    )
    # 40b
    primary_tillage_equipment_write_in = forms.CharField(
        label="28b. If you selected other, please explain.",
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=500,
        required=False,
    )
    # 41	"Secondary tillage equipment (select all that apply) for cash crop preceding the cover crop?
    secondary_tillage_equipment = forms.ChoiceField(
        label="29a. Secondary tillage equipment (select all that apply) for cash crop preceding the cover crop?",
        choices=SecondaryTillageEquipmentChoices.choices,
        required=False,
    )
    secondary_tillage_equipment_write_in = forms.CharField(
        label="29b. If you selected other, please explain.",
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=500,
        required=False,
    )

    # 42	"Soil conditions in this field at cover crop seeding
    soil_conditions_at_cover_crop_seeding = forms.ChoiceField(
        label="31. Soil conditions in this field at cover crop seeding.",
        choices=SoilConditionsSeedingChoices.choices,
        required=True,
    )

    # 43	"Cover Crop Seeding Method.
    cover_crop_seeding_method = forms.ChoiceField(
        label="32a. Please select the seeding method for the cover crop in this field.",
        choices=SeedingMethodChoices.choices,
        required=True,
    )

    # 43 b
    cover_crop_seeding_method_write_in = forms.CharField(
        label="32b. If you selected other, please explain.",
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=500,
        required=False,
    )

    # 44
    cover_crop_seed_cost = forms.IntegerField(
        label="33. Estimated cover crop seed cost for this field ($/acre)",
        min_value=0,
        required=True,
    )
    # 45	Estimated cover crop planting cost per acre in this field. Please use UW Extension Custom Rate Guide.(https://www.nass.usda.gov/Statistics_by_State/Wisconsin/Publications/WI-CRate20.pdf)
    cover_crop_planting_cost = forms.IntegerField(
        label='34. Estimated cover crop planting cost per acre in this field. Please use <a href="https://www.nass.usda.gov/Statistics_by_State/Wisconsin/Publications/WI-CRate20.pdf" target="_blank" rel="noopener noreferrer">UW Extension Custom Rate Guide.</a>',
        min_value=0,
        required=True,
    )

    class Meta:
        model = SurveyField
        fields = (
            "crop_rotation_2021_cover_crop_species",
            "crop_rotation_2021_cash_crop_species",
            "crop_rotation_2022_cover_crop_species",
            "crop_rotation_2022_cash_crop_species",
            "crop_rotation_2023_cover_crop_species",
            "crop_rotation_2023_cash_crop_species",
            "cover_crop_species_1",
            "cover_crop_planting_rate_1",
            "cover_crop_planting_rate_1_units",
            "cover_crop_species_2",
            "cover_crop_planting_rate_2",
            "cover_crop_planting_rate_2_units",
            "cover_crop_species_3",
            "cover_crop_planting_rate_3",
            "cover_crop_planting_rate_3_units",
            "cover_crop_species_4",
            "cover_crop_planting_rate_4",
            "cover_crop_planting_rate_4_units",
            "cover_crop_species_5",
            "cover_crop_planting_rate_5",
            "cover_crop_planting_rate_5_units",
            "crop_rotation",
            # "cover_crop_species_and_rate_write_in",
            # "cover_crop_multispecies_mix_write_in",
            "cash_crop_planting_date",
            # "years_with_cover_crops",
            "cover_crop_planting_date",
            "cover_crop_estimated_termination",
            "days_between_crop_hvst_and_cc_estd",
            "dominant_soil_texture",
            "manure_prior",
            "manure_prior_rate",
            "manure_prior_rate_units",
            "manure_post",
            "manure_post_rate",
            "manure_post_rate_units",
            "tillage_system_cash_crop",
            "primary_tillage_equipment",
            "primary_tillage_equipment_write_in",
            "secondary_tillage_equipment",
            "secondary_tillage_equipment_write_in",
            "soil_conditions_at_cover_crop_seeding",
            "cover_crop_seeding_method",
            "cover_crop_seeding_method_write_in",
            "cover_crop_seed_cost",
            "cover_crop_planting_cost",
        )


class SurveyFarmFormSection2(forms.ModelForm):

    # 1. Total acres of cover crops
    total_acres = forms.IntegerField(
        label="1. Total acres you planted to cover crops this year.",
        required=True,
        min_value=0,
        max_value=100000,
    )

    # 2. Percent acres of your farm in cc?
    percent_of_farm_cc = forms.IntegerField(
        label="2. What percent of all your farm acres did you plant to covers this year?",
        required=True,
        min_value=0,
        max_value=100,
    )

    # 3. Years Experience
    years_experience = forms.IntegerField(
        label="3. How many years' of experience do you have planting cover crops?",
        required=True,
        min_value=0,
        max_value=100,
    )

    # Modified to scenario choices 2025
    main_cc_goal_this_year = forms.ChoiceField(
        label="4. For the field you plan to sample a cover crop from, please select the top goal for why you are growing cover this year.",
        choices=TopGoalChoices.choices,
        required=True,
        initial=TopGoalChoices.BLANK,
    )
    
    # new 2025
    main_cc_goal_this_year_write_in = forms.CharField(
        label="4a. If you selected 'other', please describe your top goal. Please also share any other goals or thoughts on why you are growing cover crops this year.",
        required=False,
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=1000,
    )

    satisfied_with_cc_results = forms.ChoiceField(
        label="5. How satisfied are you with the results you get from cover cropping? Please select your level of satisfaction.",
        required=True,
        choices=HowSatisfiedChoices.choices,
        initial=HowSatisfiedChoices.BLANK
    )

    satisfied_with_cc_results_write_in = forms.CharField(
        label="5a. Please explain your level of satisfaction.",
        required=False,
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=1000,
    )

    barriers_to_expansion = forms.ChoiceField(
        label="6. Would you like to expand the number of acres you cover crop?",
        required=False,
        choices=ExpandAcresChoices.choices,
    )

    # New 2025
    barriers_to_expansion_write_in = forms.CharField(
        label="6a. If you chose “other” please provide details.",
        required=False,
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=1000,
    )


    biggest_challenge_cc = forms.CharField(
        label="7. What is your biggest challenge or unanswered question when it comes to cover cropping?",
        required=True,
        max_length=500,
        widget=forms.Textarea(attrs={"rows": 5}),
    )

    biggest_challenge_cc_changed_over_time = forms.CharField(
        label="7a. Have these challenges changed with time?",
        required=True,
        max_length=500,
        widget=forms.Textarea(attrs={"rows": 5}),
    )

    conservation_programs = forms.ChoiceField(
        label="8. Are you enrolled, or have you recently enrolled in Federal conservation programs such as EQIP, or CSP, or state or county programs that support your conservation practices? Which ones?",
        required=False,
        choices=TRUE_FALSE_CHOICES
    )

    conservation_programs_which_ones = forms.CharField(
        label="8a. If yes, which ones?",
        required=False,
        max_length=500,
        widget=forms.Textarea(attrs={"rows": 5}),
    )

    conservation_programs_if_helped_how = forms.CharField(
        label="8b. If government/agency conservation programs have helped you use cover crops, please explain.",
        required=False,
        max_length=500,
        widget=forms.Textarea(attrs={"rows": 5}),
    )


    def clean(self):
        super().clean()
        main_cc_goal_this_year = self.cleaned_data.get("main_cc_goal_this_year")
        main_cc_goal_this_year_write_in = self.cleaned_data.get("main_cc_goal_this_year_write_in")
        if main_cc_goal_this_year == "OTHER":
            if main_cc_goal_this_year_write_in == "":
                msg = "Since you selected 'other', please supply a bit more information about your goals."
                self.add_error("main_cc_goal_this_year_write_in", msg)                               


    class Meta:
        model = SurveyFarm
        fields = (
            "total_acres",
            "percent_of_farm_cc",
            "years_experience",
            "main_cc_goal_this_year",
            "main_cc_goal_this_year_write_in",
            "satisfied_with_cc_results",
            "satisfied_with_cc_results_write_in",
            "barriers_to_expansion",
            "barriers_to_expansion_write_in",
            
            "biggest_challenge_cc",
            "biggest_challenge_cc_changed_over_time",

            "conservation_programs",
            "conservation_programs_which_ones",
            "conservation_programs_if_helped_how",
        )


class FieldFarmFormSection3(forms.ModelForm):
    """For static data about a farmer's field"""

    field_name = forms.CharField(
        label="Please enter a name for this field", required=False, max_length=250
    )
    # 16 Closest zip code for this field (so we can determine appropriate climate data and generate a location map of participating fields). Field must be located in Wisconsin.
    closest_zip_code = forms.IntegerField(
        label="9. Enter the closest zip code for this field.",
        required=True,
        min_value=0,
        max_value=99999,
    )
    # 18 What is this field(s) acreage?
    field_acreage = forms.IntegerField(
        label="10. What is this field's acreage?", required=True, min_value=0
    )
    # 19 In the following section we ask you about your specific cover cropping practices in one field or set of fields (can be one acre ro 1,000) from which you'll take your samples for biomass, nutrient, and forage analysis. Provide answers *for that field.*
    field_location = geo_forms.PointField(
        label="11. Zoom in to the map and click the general location for this field.",
        help_text="To reset the location, click 'Delete all features' and click a different location",
        widget=geo_forms.OSMWidget(
            attrs={
                "default_lat": 44.636774,
                "default_lon": -90.012530,
                "default_zoom": 6,
            }
        ),
        required=False,
    )

    class Meta:
        model = FieldFarm
        fields = (
            "field_name",
            "closest_zip_code",
            "field_acreage",
            "field_location",
        )


class SurveyFieldFormSection3(forms.ModelForm):

    crop_rotation_2021_cash_crop_species = forms.ChoiceField(
        label="12a. Cash crop planted 2023",
        choices=CashCropChoices.choices,
        required=True,
        initial=CashCropChoices.BLANK,
    )

    crop_rotation_2021_cover_crop_species = forms.ChoiceField(
        label="12b. Cover crop planted 2023",
        choices=CoverCropChoicesWMulti.choices,
        required=True,
        initial=CoverCropChoices.BLANK,
    )

    # 21 a.
    crop_rotation_2022_cash_crop_species = forms.ChoiceField(
        label="13a. Cash crop planted 2024",
        choices=CashCropChoices.choices,
        required=True,
    )
    # 21 b
    crop_rotation_2022_cover_crop_species = forms.ChoiceField(
        label="13b. Cover crop planted 2024",
        choices=CoverCropChoicesWMulti.choices,
        required=True,
        initial=CoverCropChoices.BLANK,
    )
    # 22 a.
    crop_rotation_2023_cash_crop_species = forms.ChoiceField(
        label="14a. Cash crop planted 2025",
        choices=CashCropChoices.choices,
        required=True,
    )
    # 22 b.
    crop_rotation_2023_cover_crop_species = forms.ChoiceField(
        label="14b. Cover crop planted 2025",
        choices=CoverCropChoicesWMulti.choices,
        required=True,
    )

    # Question 18, labeled as such in the form_ html
    # Species 1
    cover_crop_species_1 = forms.ChoiceField(
        label="a. Species",
        choices=CoverCropChoices.choices,
        required=True,
    )
    # 24b
    cover_crop_planting_rate_1 = forms.DecimalField(
        label="b. Planting rate", required=True, max_value=1000, min_value=0
    )
    # 24c
    cover_crop_planting_rate_1_units = forms.ChoiceField(
        label="c. Planting rate units",
        choices=CoverCropRateUnitsChoices.choices,
        required=True,
    )
    # Species 2
    # 25a
    cover_crop_species_2 = forms.ChoiceField(
        label="d. Species",
        choices=CoverCropChoices.choices,
        required=False,
    )
    # 25b
    cover_crop_planting_rate_2 = forms.DecimalField(
        label="e. Planting rate", required=False, max_value=1000, min_value=0
    )
    # 25c
    cover_crop_planting_rate_2_units = forms.ChoiceField(
        label="f. Planting rate units",
        choices=CoverCropRateUnitsChoices.choices,
        required=False,
    )
    # Species 3
    # 26
    cover_crop_species_3 = forms.ChoiceField(
        label="g. Species",
        choices=CoverCropChoices.choices,
        required=False,
    )
    cover_crop_planting_rate_3 = forms.DecimalField(
        label="h. Planting rate", required=False, max_value=1000, min_value=0
    )
    cover_crop_planting_rate_3_units = forms.ChoiceField(
        label="i. Planting rate units",
        choices=CoverCropRateUnitsChoices.choices,
        required=False,
    )
    # Species 4
    # 27
    cover_crop_species_4 = forms.ChoiceField(
        label="j. Species",
        choices=CoverCropChoices.choices,
        required=False,
    )
    cover_crop_planting_rate_4 = forms.DecimalField(
        label="k. Planting rate", required=False, max_value=1000, min_value=0
    )
    cover_crop_planting_rate_4_units = forms.ChoiceField(
        label="l. Planting rate units",
        choices=CoverCropRateUnitsChoices.choices,
        required=False,
    )
    # Species 5
    # 28
    cover_crop_species_5 = forms.ChoiceField(
        label="m. Species",
        choices=CoverCropChoices.choices,
        required=False,
    )
    cover_crop_planting_rate_5 = forms.DecimalField(
        label="n. Planting rate", required=False, max_value=1000, min_value=0
    )
    cover_crop_planting_rate_5_units = forms.ChoiceField(
        label="o. Planting rate units",
        choices=CoverCropRateUnitsChoices.choices,
        required=False,
    )
    # 23	"Please describe your crop rotation for this field including cover crops.
    crop_rotation = forms.CharField(
        label="16. Please share any other details about your crop rotation and cover crop planting rates.",
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=500,
        required=False,
    )

    # def clean(self):
    #     super().clean()
    #     addlt_species = [
    #         ("cover_crop_species_2", "cover_crop_planting_rate_2", "cover_crop_planting_rate_2_units"),
    #         ("cover_crop_species_3", "cover_crop_planting_rate_3", "cover_crop_planting_rate_3_units"),
    #         ("cover_crop_species_4", "cover_crop_planting_rate_4", "cover_crop_planting_rate_4_units"),
    #         ("cover_crop_species_5", "cover_crop_planting_rate_5", "cover_crop_planting_rate_5_units"),
    #         ]
    #     for addlt_tuple in addlt_species:
    #         species = self.cleaned_data.get(addlt_tuple[0])
    #         rate = self.cleaned_data.get(addlt_tuple[1])
    #         unit = self.cleaned_data.get(addlt_tuple[2])

    #     cover_crop_species_2 = self.cleaned_data.get("cover_crop_species_2")
    #     cover_crop_planting_rate_2 = self.cleaned_data.get("cover_crop_planting_rate_2")
    #     cover_crop_planting_rate_2_units = self.cleaned_data.get("cover_crop_planting_rate_2_units")
        
        

    class Meta:
        model = SurveyField
        fields = (
            "crop_rotation_2021_cover_crop_species",
            "crop_rotation_2021_cash_crop_species",
            "crop_rotation_2022_cover_crop_species",
            "crop_rotation_2022_cash_crop_species",
            "crop_rotation_2023_cover_crop_species",
            "crop_rotation_2023_cash_crop_species",
            "crop_rotation",
            "cover_crop_species_1",
            "cover_crop_planting_rate_1",
            "cover_crop_planting_rate_1_units",
            "cover_crop_species_2",
            "cover_crop_planting_rate_2",
            "cover_crop_planting_rate_2_units",
            "cover_crop_species_3",
            "cover_crop_planting_rate_3",
            "cover_crop_planting_rate_3_units",
            "cover_crop_species_4",
            "cover_crop_planting_rate_4",
            "cover_crop_planting_rate_4_units",
            "cover_crop_species_5",
            "cover_crop_planting_rate_5",
            "cover_crop_planting_rate_5_units",
        )


class SurveyFieldFormSection4_part1(forms.ModelForm):

    # 31	What date this year did you plant your cash crop in this field?
    cash_crop_planting_date = forms.DateField(
        label="17. What date did you plant your cash crop in this field? (Approximate date is fine if you aren't sure.)",
        required=True,
    )

    class Meta:
        model = SurveyField
        fields = ("cash_crop_planting_date",)


class SurveyFarmFormSection4(forms.ModelForm):

    
    cover_crops_delay_cash_crop = forms.ChoiceField(
        label="REMOVE THIS SOMEHOW! QUESTION DEPRECATED. 21. Does planting a cover crop delay when you would otherwise plant your cash crop?",
        choices=TRUE_FALSE_CHOICES,
        required=False,
    )

    class Meta:
        model = SurveyFarm
        fields = ("cover_crops_delay_cash_crop",)



class SurveyFieldFormSection4_part2(forms.ModelForm):

    # 46	Cover crop planting date for this field (estimate is OK if not known).
    cover_crop_planting_date = forms.DateField(
        label="18. Cover crop planting date for this field (estimate is OK if not known).",
        required=True,
    )
    # 47	"Estimated termination timing/method for this field.
    cover_crop_estimated_termination = forms.ChoiceField(
        label="19a. Estimated termination timing/method for this field.",
        choices=TerminationMethodTimingChoices.choices,
        required=True,
    )

    cover_crop_estimated_termination_write_in = forms.CharField(
        label="19b. Please explain if you selected other.",
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=500,
        required=False,
    )

    # 48	Number of days estimated between crop harvest and cover crop establishment in this field.
    days_between_crop_hvst_and_cc_estd = forms.IntegerField(
        label="20. Number of days estimated between crop harvest and cover crop establishment in this field.",
        min_value=0,
        max_value=365,
        required=True,
    )

    class Meta:
        model = SurveyField
        fields = (
            "cover_crop_planting_date",
            "cover_crop_estimated_termination",
            "cover_crop_estimated_termination_write_in",
            "days_between_crop_hvst_and_cc_estd",
        )


class SurveyFieldFormSection5(forms.ModelForm):

    
    manure_prior = forms.ChoiceField(
        label="21a. Will you or did you apply manure prior to seeding cover crops on this field?",
        required=True,
        choices=TRUE_FALSE_CHOICES,
    )
    
    manure_prior_rate = forms.IntegerField(
        label="21b. At what rate will the manure be applied?",
        required=False,
        min_value=0,
    )
    
    manure_prior_rate_units = forms.ChoiceField(
        label="21c. Please select the units for the manure application rate.",
        choices=ManureApplicateUnitsChoices.choices,
        required=False,
    )

    manure_prior_source = forms.ChoiceField(
        label="21d. Please select the source of the manure.",
        choices=ManureSourceChoices.choices,
        required=False,
    )

    manure_prior_consistency = forms.ChoiceField(
        label="21e. Please select the consistency of the manure.",
        choices=ManureConsistencyChoices.choices,
        required=False,
    )
    
    
    manure_post = forms.ChoiceField(
        label="22a. Will manure be applied to the field after the cover crop is established?",
        required=True,
        choices=TRUE_FALSE_CHOICES,
    )
    
    manure_post_rate = forms.IntegerField(
        label="22b. At what rate will the manure be applied?",
        required=False,
        min_value=0,
    )
    
    manure_post_rate_units = forms.ChoiceField(
        label="22c. The units for the manure application rate",
        choices=ManureApplicateUnitsChoices.choices,
        required=False,
    )

    manure_post_source = forms.ChoiceField(
        label="22d. Please select the source of the manure.",
        choices=ManureSourceChoices.choices,
        required=False,
    )

    manure_post_consistency = forms.ChoiceField(
        label="22e. Please select the consistency of the manure.",
        choices=ManureConsistencyChoices.choices,
        required=False,
    )

    # New 2025
    synth_fert_for_covers = forms.ChoiceField(
        label="23. Did you apply synthetic fertilizer for growing a cover crop?",
        choices=TRUE_FALSE_CHOICES,
        required=True
    )
    # New 2025
    synth_fert_for_covers_application_date = forms.DateField(
        label="23a. If yes, what is the estimated date of the application?",
        required=False
    )

    # 39	"What is your tillage system for the cash crop preceding the cover crop?
    tillage_system_cash_crop = forms.ChoiceField(
        label="24. What is your tillage system for the cash crop preceding the cover crop?",
        choices=TillageSystemChoices.choices,
        required=True,
    )
    # 40a	"Primary tillage equipment (select all that apply) for a cash crop preceding a cover crop?
    primary_tillage_equipment = forms.ChoiceField(
        label="25a. Primary tillage equipment (select all that apply) for a cash crop preceding a cover crop?",
        choices=PrimaryTillageEquipmentChoices.choices,
        required=True,
    )
    # 40b
    primary_tillage_equipment_write_in = forms.CharField(
        label="25b. If you selected other, please explain.",
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=500,
        required=False,
    )
    # 41	"Secondary tillage equipment (select all that apply) for cash crop preceding the cover crop?
    secondary_tillage_equipment = forms.ChoiceField(
        label="26a. Secondary tillage equipment (select all that apply) for cash crop preceding the cover crop?",
        choices=SecondaryTillageEquipmentChoices.choices,
        required=False,
    )
    secondary_tillage_equipment_write_in = forms.CharField(
        label="26b. If you selected other, please explain.",
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=500,
        required=False,
    )
    # 33	"Please choose the dominant soil texture of the field.
    dominant_soil_texture = forms.ChoiceField(
        label="27. Please select the dominant soil texture of this field.",
        choices=SoilTextureClassChoices.choices,
        required=True,
    )
    # 42	"Soil conditions in this field at cover crop seeding
    soil_conditions_at_cover_crop_seeding = forms.ChoiceField(
        label="28. Soil conditions in this field at cover crop seeding.",
        choices=SoilConditionsSeedingChoices.choices,
        required=True,
    )

    def clean(self):
        super().clean()
        manure_prior = self.cleaned_data.get("manure_prior")
        manure_prior_rate = self.cleaned_data.get("manure_prior_rate")
        manure_prior_rate_units = self.cleaned_data.get("manure_prior_rate_units")
        manure_prior_source = self.cleaned_data.get("manure_prior_source")
        manure_prior_consistency = self.cleaned_data.get("manure_prior_consistency")
        # print("Manure prior rate units:")
        # print("\t", manure_prior_rate_units)
        # print("\t", type(manure_prior_rate_units))
        # print("\tis equal to ''", manure_prior_rate_units == "")
        # print("Manure prior rate units:")
        # print("\t", manure_prior_source)
        # print("\t", type(manure_prior_source))
        # print("\tis equal to ''", manure_prior_source == "")        
        manure_post = self.cleaned_data.get("manure_post")
        manure_post_rate = self.cleaned_data.get("manure_post_rate")
        manure_post_rate_units = self.cleaned_data.get("manure_post_rate_units")
        manure_post_source = self.cleaned_data.get("manure_post_source")
        manure_post_consistency = self.cleaned_data.get("manure_post_consistency")        

        # If manure is *NOT* applied prior to cc, ensure rate and units, source, consistency are *NOT* populated
        if manure_prior == "False" and (
            manure_prior_rate is not None or manure_prior_rate_units != "" or manure_prior_source != "" or manure_prior_consistency != ""
        ):
            # Rate must be 0 or None
            if manure_prior_rate is not None:
                if manure_prior_rate > 0:
                    msg = (
                        "If you are not applying manure, please enter 0 or leave blank."
                    )
                    self.add_error("manure_prior_rate", msg)

            if manure_prior_rate_units != "":
                msg = "If you are not applying manure, please leave blank."
                self.add_error("manure_prior_rate_units", msg)
            if manure_prior_source != "":
                msg = "If you are not applying manure, please leave blank."
                self.add_error("manure_prior_source", msg)       
            if manure_prior_consistency != "":
                msg = "If you are not applying manure, please leave blank."
                self.add_error("manure_prior_consistency", msg)                                

        # If manure is *NOT* applied after to cc, ensure rate and units, source, consistency are *NOT* populated
        if manure_post == "False" and (
            manure_post_rate is not None or manure_post_rate_units != "" or manure_post_source != "" or manure_post_consistency != ""
        ):
            # Rate must be 0 or None
            if manure_post_rate is not None:
                if manure_post_rate > 0:
                    msg = (
                        "If you are not applying manure, please enter 0 or leave blank."
                    )
                    self.add_error("manure_post_rate", msg)

            if manure_post_rate_units != "":
                msg = "If you are not applying manure, please leave blank."
                self.add_error("manure_post_rate_units", msg)

            if manure_post_source != "":
                msg = "If you are not applying manure, please leave blank."
                self.add_error("manure_prior_source", msg)       

            if manure_post_consistency != "":
                msg = "If you are not applying manure, please leave blank."
                self.add_error("manure_prior_consistency", msg)             

        # If manure is applied prior to cc, ensure rate and units, source, consistency are populated
        if manure_prior == "True":
            if manure_prior_rate is None:
                msg = "Please enter a manure rate"
                self.add_error("manure_prior_rate", msg)

            if manure_prior_rate_units == "":
                msg = "Please enter the units for this manure rate"
                self.add_error("manure_prior_rate_units", msg)

            if manure_prior_source == "":
                msg = "Please enter the source of the manure"
                self.add_error("manure_prior_source", msg)

            if manure_prior_consistency == "":
                msg = "Please select the approximate moisture level of the manure"
                self.add_error("manure_prior_consistency", msg)                

        # If manure is applied after to cc, ensure rate and units, source, consistency are populated
        if manure_post == "True":
            if manure_post_rate is None:
                msg = "Please enter a manure rate"
                self.add_error("manure_post_rate", msg)

            if manure_post_rate_units == "":
                msg = "Please enter the units for this manure rate"
                self.add_error("manure_post_rate_units", msg)

            if manure_post_source == "":
                msg = "Please enter the source of the manure"
                self.add_error("manure_post_source", msg)

            if manure_post_consistency == "":
                msg = "Please select the approximate moisture level of the manure"
                self.add_error("manure_post_consistency", msg)    

        synth_fert_for_covers = self.cleaned_data.get("synth_fert_for_covers")
        synth_fert_for_covers_application_date = self.cleaned_data.get("synth_fert_for_covers_application_date")

        
        # If synth fert applied, then make sure to select a date
        if synth_fert_for_covers == "True":
            if synth_fert_for_covers_application_date is None:
                msg = "Please select the approximate date of the synthetic fertilizer application."
                self.add_error("synth_fert_for_covers_application_date", msg)    

        if synth_fert_for_covers == "False":
            if synth_fert_for_covers_application_date is not None:
                msg = "Please leave the date blank if you did not apply synthetic fertilizer."
                self.add_error("synth_fert_for_covers_application_date", msg)   

    class Meta:
        model = SurveyField
        fields = (
            "manure_prior",
            "manure_prior_rate",
            "manure_prior_rate_units",
            "manure_prior_source",
            "manure_prior_consistency",            
            "manure_post",
            "manure_post_rate",
            "manure_post_rate_units",
            "manure_post_source",
            "manure_post_consistency",
            "synth_fert_for_covers",
            "synth_fert_for_covers_application_date",
            "tillage_system_cash_crop",
            "primary_tillage_equipment",
            "primary_tillage_equipment_write_in",
            "secondary_tillage_equipment",
            "secondary_tillage_equipment_write_in",
            "soil_conditions_at_cover_crop_seeding",
            "dominant_soil_texture",
        )


class SurveyFieldFormSection6(forms.ModelForm):


    cover_crop_seeding_method = forms.ChoiceField(
        label="29a. Please select the seeding method for the cover crop in this field.",
        choices=SeedingMethodChoices.choices,
        required=True,
    )

    cover_crop_seeding_method_write_in = forms.CharField(
        label="29b. If you selected other, please explain.",
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=500,
        required=False,
    )

    # New 2025
    cover_crop_seeding_method_drone = forms.CharField(
        label="29c. If you used a drone to seed covers, what years have you used them, ie Fall 2024?",
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=500,
        required=False,
    )


    # 44
    cover_crop_seed_cost = forms.IntegerField(
        label="30. Estimated cover crop seed cost for this field ($/acre)",
        min_value=0,
        required=True,
    )
    # 45	Estimated cover crop planting cost per acre in this field. Please use UW Extension Custom Rate Guide.(https://www.nass.usda.gov/Statistics_by_State/Wisconsin/Publications/WI-CRate20.pdf)
    cover_crop_planting_cost = forms.IntegerField(
        label='31. Estimated cover crop planting cost per acre in this field. Please use <a href="https://www.nass.usda.gov/Statistics_by_State/Wisconsin/Publications/WI-CRate20.pdf" target="_blank" rel="noopener noreferrer">UW Extension Custom Rate Guide.</a>',
        min_value=0,
        required=True,
    )

    def clean(self):
        super().clean()
        cover_crop_seeding_method = self.cleaned_data.get("cover_crop_seeding_method")
        cover_crop_seeding_method_write_in = self.cleaned_data.get("cover_crop_seeding_method_write_in")

        if cover_crop_seeding_method == "OTHER":
            if cover_crop_seeding_method_write_in == "":
                msg = "Since you selected 'other', please supply a bit more information about your seeding method."
                self.add_error("cover_crop_seeding_method_write_in", msg)                               

    class Meta:
        model = SurveyField
        fields = (
            "cover_crop_seeding_method",
            "cover_crop_seeding_method_write_in",
            "cover_crop_seeding_method_drone",
            "cover_crop_seed_cost",
            "cover_crop_planting_cost",
        )


class SurveyFarmFormSection6(forms.ModelForm):
    # 35. Do you save cover crop seed?
    save_cover_crop_seed = forms.ChoiceField(
        label="32a. Do you save cover crop seed?",
        required=True,
        choices=TRUE_FALSE_CHOICES,
    )
    # 36. What is your source for cover crop seed?
    source_cover_crop_seed = forms.CharField(
        label="32b. What is your cover crop seed source?",
        required=True,
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=500,
    )

    class Meta:
        model = SurveyFarm
        fields = (
            "save_cover_crop_seed",
            "source_cover_crop_seed",
        )


class SurveyFarmFormSection7(forms.ModelForm):

    # encourage_cc = forms.ChoiceField(
    #     label="36a. Which of the following would do the most to encourage more farmers to cover crop?",
    #     choices=CoverCropSupportChoices.choices,
    #     required=True,
    # )

    # encourage_cc_write_in = forms.CharField(
    #     label="36b. Please explain.",
    #     widget=forms.Textarea(attrs={"rows": 5}),
    #     required=False,
    # )

    # additional_thoughts = forms.CharField(
    #     label="37. Any additional thoughts or questions? Any important survey questions we should ask next time?",
    #     widget=forms.Textarea(attrs={"rows": 5}),
    #     max_length=1000,
    #     required=False,
    # )

    # learn_about_other_farmers_cc = forms.CharField(
    #     label="33a. Are you interested in learning what other farmers are doing with cover crops?",
    #     widget=forms.Textarea(attrs={"rows": 5}),
    #     max_length=1000,
    #     required=False,
    # )

    learn_about_cc_preferred_way = forms.CharField(
            label="""33. What are your preferred ways to learn about using cover crops? Please be
                specific, for example, if there are particular Youtube channels, podcasts,
                consultants, or leaders in your county that have helped you.""",
            widget=forms.Textarea(attrs={"rows": 5}),
            max_length=1000,
            required=False,
    )
    # what_info_other_farmers_most_useful = forms.CharField(
    #     label="33c. What information from other farms using cover crops would be most useful to you?",
    #     widget=forms.Textarea(attrs={"rows": 5}),
    #     max_length=1000,
    #     required=False,
    # )

    scenario_tool_feedback = forms.CharField(
        label="""34. We created an online "Cover Crop Scenario Tool" to share the cover crop
practices gathered by this project for the last 5 years. The tool can be found 
<a href="https://evansgeospatial.com/wisc_cc_scenario" target="_blank" rel="noopener noreferrer">here</a>.
Please provide us with any
feedback as we are in the testing phase. Your opinion is important. """,
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=1000,
        required=False,
    )

    # scenario_tool_easy_to_use = forms.CharField(
    #     label="34a. Did you find the scenario tool easy to use or not and why?",
    #     widget=forms.Textarea(attrs={"rows": 5}),
    #     max_length=1000,
    #     required=False,
    # )

    # scenario_tool_return_to_tool = forms.CharField(
    #     label="34b. Do you imagine returning to use this in the future? Please explain why or why not.",
    #     widget=forms.Textarea(attrs={"rows": 5}),
    #     max_length=1000,
    #     required=False,
    # )

    # scenario_tool_lacking_info = forms.CharField(
    #     label="34c. Is there information on cover cropping you are most interested in that you don't find in the scenario tool?",
    #     widget=forms.Textarea(attrs={"rows": 5}),
    #     max_length=1000,
    #     required=False,
    # )

    testimonial = forms.CharField(
        label="""35a. For outreach efforts around this project, 
please share anything regarding your experience with the project or
 with cover cropping we might use. 
 <br>How would you describe why you joined this project,
   and what your experience has been? Why is cover cropping important? 
   Has this project changed what you know about cover cropping?""",
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=1000,
        required=False,
    )

    willing_to_share_more = forms.ChoiceField(
        label="""35b. Can we attribute this to you or do you prefer to remain anonymous?""",
        required=True,
        choices=TRUE_FALSE_CHOICES_SHARE_OR_ANON
    )

    class Meta:
        model = SurveyFarm
        fields = (
            # "learn_about_other_farmers_cc",
            "learn_about_cc_preferred_way",
            # "what_info_other_farmers_most_useful",
            "scenario_tool_feedback",
            # "scenario_tool_easy_to_use",
            # "scenario_tool_return_to_tool",
            # "scenario_tool_lacking_info",
            "testimonial",
            "willing_to_share_more",
        )


class SurveyFarmFormReview(forms.ModelForm):

    notes_admin = forms.CharField(
        label="Notes about survey response (for admin purposes)",
        widget=forms.Textarea,
        max_length=5000,
        required=False,
    )

    confirmed_accurate = forms.ChoiceField(
        label="Is all the information in this entry accurate?",
        required=False,
        choices=TRUE_FALSE_CHOICES,
    )

    class Meta:
        model = SurveyFarm
        fields = (
            "confirmed_accurate",
            "notes_admin",
        )


class SurveyPhotoForm(forms.ModelForm):

    image_1 = forms.FileField(label="Photo 1", required=False)
    caption_photo_1 = forms.CharField(
        label="Add a caption to be displayed with photo 1.",
        required=False,
        max_length=50,
        initial="",
    )
    image_2 = forms.FileField(label="Photo 2", required=False)
    caption_photo_2 = forms.CharField(
        label="Add a caption to be displayed with photo 2.",
        required=False,
        max_length=50,
        initial="",
    )

    spring_image_1 = forms.FileField(label="Spring Photo 1", required=False)
    spring_caption_photo_1 = forms.CharField(
        label="Add a caption to be displayed with Spring photo 1.",
        required=False,
        max_length=50,
        initial="",
    )
    spring_image_2 = forms.FileField(label="Spring Photo 2", required=False)
    spring_caption_photo_2 = forms.CharField(
        label="Add a caption to be displayed with Spring photo 2.",
        required=False,
        max_length=50,
        initial="",
    )


    notes = forms.CharField(
        label="Add any notes about these photos, notes will not be displayed.",
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control form-control-lg",
            },
        ),
        required=False,
    )

    class Meta:
        model = SurveyPhoto
        fields = ["image_1", "caption_photo_1", "image_2", "caption_photo_2",
                  "spring_image_1", "spring_caption_photo_1", "spring_image_2", "spring_caption_photo_2", "notes"]


class CustomUserCreationForm(UserCreationForm):
    email = forms.CharField(
        label="Email (this will be your username as well)",
        max_length=254,
        required=True,
        widget=forms.EmailInput(),
    )

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        client_ip = kwargs["initial"]["client_ip"]
        super().__init__(*args, **kwargs)
        self.fields["turnstile"] = TurnstileField(client_ip=client_ip)
        self.fields["turnstile"].widget = forms.HiddenInput()

    def clean_username(self):
        username = self.cleaned_data["username"].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError(
                """Email already exists. Perhaps you have already created an account. Try using this email address to reset your password."""
            )
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data["email"],
            self.cleaned_data["email"],
            self.cleaned_data["password1"],
        )
        return user


class SurveyRegistrationFullForm(forms.ModelForm):
    """For updating or reviewing signing up for survey and biomass kit"""

    belong_to_groups = forms.CharField(
        label="If you belong to a producer-led watershed protection group or other agricultural conservation group what is the name of the group?",
        required=False,
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=500,
    )
    howd_you_hear = forms.CharField(
        label="How did you hear about the project?",
        required=False,
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=500,
    )
    notes = forms.CharField(
        label="Admin notes",
        required=False,
        widget=forms.Textarea(attrs={"rows": 10}),
        max_length=1000,
    )
    biomass_or_just_survey = forms.ChoiceField(
        label="Are you interested in sampling for biomass in addition to filling out a survey?",
        required=True,
        choices=SurveyRegistration.BiomassOrJustSurveyChoices.choices,
        widget=forms.RadioSelect,
    )
    do_you_have_a_biomas_kit = forms.ChoiceField(
        label="If you have agreed to sample, do you have a biomass sampling kit from previous years?",
        choices=SurveyRegistration.HaveAKit.choices,
        required=True,
        widget=forms.RadioSelect,
    )
    do_you_need_assistance = forms.CharField(
        label="If you prefer a paper copy of the survey mailed to you, or would like assistance with filling out the online survey, or with biomass collection, please let us know in the box below.?",
        required=False,
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=500,
    )
    privacy_consent = forms.ChoiceField(
        label="If you agree to this statement above click yes and proceed to the survey.",
        choices=TRUE_FALSE_CHOICES,
        required=False,
    )

    class Meta:
        model = SurveyRegistration
        fields = [
            "belong_to_groups",
            "howd_you_hear",
            "notes",
            "biomass_or_just_survey",
            "do_you_have_a_biomas_kit",
            "do_you_need_assistance",
            "privacy_consent",
        ]


class SurveyRegistrationPartialForm(forms.ModelForm):
    """For updating or reviewing signing up for survey and biomass kit"""

    belong_to_groups = forms.CharField(
        label="If you belong to a producer-led watershed protection group or other agricultural conservation group what is the name of the group?",
        required=False,
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=500,
    )
    howd_you_hear = forms.CharField(
        label="How did you hear about the project?",
        required=False,
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=500,
    )
    biomass_or_just_survey = forms.ChoiceField(
        label="Are you interested in sampling for biomass in addition to filling out a survey?",
        required=True,
        choices=SurveyRegistration.BiomassOrJustSurveyChoices.choices,
        widget=forms.RadioSelect,
    )
    do_you_have_a_biomas_kit = forms.ChoiceField(
        label="If you have agreed to sample, do you have a biomass sampling kit from previous years?",
        choices=SurveyRegistration.HaveAKit.choices,
        required=True,
        widget=forms.RadioSelect,
    )
    do_you_need_assistance = forms.CharField(
        label="If you prefer a paper copy of the survey mailed to you, or would like assistance with filling out the online survey, or with biomass collection, please let us know in the box below.?",
        required=False,
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=500,
    )
    privacy_consent = forms.ChoiceField(
        label="If you agree to this statement above click yes and proceed to the survey.",
        choices=TRUE_FALSE_CHOICES,
        required=True,
    )

    class Meta:
        model = SurveyRegistration
        fields = [
            "belong_to_groups",
            "howd_you_hear",
            "biomass_or_just_survey",
            "do_you_have_a_biomas_kit",
            "do_you_need_assistance",
            "privacy_consent",
        ]


class UserInfoForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["username", "email"]


class ResearcherSignupForm(forms.ModelForm):
    """For creating collaborating researchers"""

    first_name = forms.CharField(max_length=250, required=True)
    last_name = forms.CharField(max_length=250, required=True)
    institution = forms.CharField(
        label="What institution is this researcher affiliated with?",
        required=False,
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=500,
    )
    notes = forms.CharField(
        label="Notes about researcher",
        required=False,
        widget=forms.Textarea(attrs={"rows": 10}),
        max_length=500,
    )
    agreement_doc = forms.FileField(label="Upload agreement docs", required=False)
    approved = forms.ChoiceField(
        label="Approve this researcher for a year download permissions?",
        required=True,
        choices=TRUE_FALSE_CHOICES,
    )
    approved_date = forms.DateField(
        label="Date approved. Permissions expire one year after this date.",
        required=False,
    )

    class Meta:
        model = Researcher
        fields = [
            "first_name",
            "last_name",
            "institution",
            "notes",
            "agreement_doc",
            "approved",
            "approved_date",
        ]


class ResearcherFullForm(forms.ModelForm):
    """For creating collaborating researchers"""

    first_name = forms.CharField(max_length=250, required=False)
    last_name = forms.CharField(max_length=250, required=False)
    institution = forms.CharField(
        label="What institution is this researcher affiliated with?",
        required=False,
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=500,
    )
    notes = forms.CharField(
        label="Notes about researcher",
        required=False,
        widget=forms.Textarea(attrs={"rows": 10}),
        max_length=500,
    )
    agreement_doc = forms.FileField(label="Upload agreement docs", required=False)
    approved = forms.ChoiceField(
        label="Approve this researcher for a year download permissions?",
        required=False,
        choices=TRUE_FALSE_CHOICES,
    )
    approved_date = forms.DateField(
        label="Date approved. Permissions expire one year after this date.",
        required=False,
    )
    download_count = forms.IntegerField(required=False)
    last_download_timestamp = forms.DateTimeField(required=False)

    class Meta:
        model = Researcher
        fields = [
            "first_name",
            "last_name",
            "institution",
            "notes",
            "agreement_doc",
            "approved",
            "approved_date",
            "download_count",
            "last_download_timestamp",
        ]


class AncillaryDataForm(forms.ModelForm):

    biomass_collection_date = forms.DateField(
        required=False, label="Fall biomass collection date"
    )
    height_of_stand = forms.DecimalField(
        decimal_places=2,
        max_digits=15,
        label="FALL Height of cover crop stand stand (in)",
        required=False,
    )
    spring_height_of_stand = forms.DecimalField(
        decimal_places=2,
        max_digits=15,
        label="Spring height of cover crop stand stand (in)",
        required=False,
    )
    cp = forms.DecimalField(
        decimal_places=2, max_digits=15, label="Fall Crude protein", required=False
    )
    andf = forms.DecimalField(
        decimal_places=2, max_digits=15, label="Fall ANDF", required=False
    )
    undfom30 = forms.DecimalField(
        decimal_places=2, max_digits=15, label="Fall undfom30", required=False
    )
    ndfd30 = forms.DecimalField(
        decimal_places=2, max_digits=15, label="Fall ndfd30", required=False
    )
    tdn_adf = forms.DecimalField(
        decimal_places=2, max_digits=15, label="Fall tdn_adf", required=False
    )
    milk_ton_milk2013 = forms.DecimalField(
        decimal_places=2, max_digits=15, label="Fall Milk_ton_milk2013", required=False
    )
    rfq = forms.DecimalField(
        decimal_places=2,
        max_digits=15,
        label="Fall Relative forage quality (RFQ)",
        required=False,
    )

    undfom240 = forms.DecimalField(
        decimal_places=2,
        max_digits=15,
        label="Fall uNDFOM240",
        required=False,
    )
    dry_matter = forms.DecimalField(
        decimal_places=2,
        max_digits=15,
        label="Fall dry_matter (%)",
        required=False,
    )
    adf = forms.DecimalField(
        decimal_places=2,
        max_digits=15,
        label="Fall acid detergent fiber",
        required=False,
    )
    rfv = forms.DecimalField(
        decimal_places=2,
        max_digits=15,
        label="Fall Relative forage value (RFV)",
        required=False,
    )
    cc_biomass = forms.DecimalField(
        decimal_places=2,
        max_digits=15,
        label="Fall Cover crop biomass, english tons dry matter per acre",
        required=False,
    )

    c_to_n_ratio = forms.DecimalField(
        decimal_places=2,
        max_digits=5,
        label="Fall C to N ratio, agsource",
        required=False,
    )
    
    percent_p = forms.DecimalField(
        decimal_places=2,
        max_digits=7,
        label="Phosphorus content as percent of dry matter, agsource",
        required=False,
    )
    percent_k = forms.DecimalField(
        decimal_places=2,
        max_digits=7,
        label="Potassium content as percent of dry matter, agsource",
        required=False,
    )    
    percent_ca = forms.DecimalField(
        decimal_places=2,
        max_digits=7,
        label="Calcium content as percent of dry matter, agsource",
        required=False,
    )        
    percent_mg = forms.DecimalField(
        decimal_places=2,
        max_digits=7,
        label="Magnesium content as percent of dry matter, agsource",
        required=False,
    )         
    percent_s = forms.DecimalField(
        decimal_places=2,
        max_digits=7,
        label="Sulfur content as percent of dry matter, agsource",
        required=False,
    )               
    p_content = forms.DecimalField(
        decimal_places=2,
        max_digits=7,
        label="Phosphate (P2O5) content of forage if 100% dry matter, lbs/acre; agsource",
        required=False,
    )
    n_content = forms.DecimalField(
        decimal_places=2,
        max_digits=7,
        label="Nitrogen content of forage if 100% dry matter, lbs/acre; agsource",
        required=False,
    )    
    k_content = forms.DecimalField(
        decimal_places=2,
        max_digits=7,
        label="Potash (K2O) content of forage if 100% dry matter, lbs/acre; agsource",
        required=False,
    )    
    ca_content = forms.DecimalField(
        decimal_places=2,
        max_digits=7,
        label="Calcium content of forage if 100% dry matter, lbs/acre; agsource",
        required=False,
    )        
    mg_content = forms.DecimalField(
        decimal_places=2,
        max_digits=7,
        label="Magnesium content of forage if 100% dry matter, lbs/acre; agsource",
        required=False,
    )         
    s_content = forms.DecimalField(
        decimal_places=2,
        max_digits=7,
        label="Sulfur content of forage if 100% dry matter, lbs/acre; agsource",
        required=False,
    )
    c_content = forms.DecimalField(
        decimal_places=2,
        max_digits=7,
        label="Carbon content of forage if 100% dry matter, lbs/acre; agsource",
        required=False,
    )


    total_nitrogen = forms.DecimalField(
        decimal_places=2, max_digits=15, label="Fall, nitrogen content as percent of dry matter, agsource", required=False
    )

    acc_gdd = forms.DecimalField(
        decimal_places=2,
        max_digits=15,
        label="Fall Accumulated growing degree units",
        required=False,
    )
    total_precip = forms.DecimalField(
        decimal_places=2,
        max_digits=15,
        label="Fall Total precipitation, in inches",
        required=False,
    )
    fall_notes = forms.CharField(
        label="Text to be displayed regarding fall biomass sampling or lab processing.",
        required=False,
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=1000,
    )
    spring_biomass_collection_date = forms.DateField(
        required=False, label="Spring biomass collection date"
    )
    spring_cc_biomass = forms.DecimalField(
        decimal_places=2,
        max_digits=15,
        label="Spring cover crop biomass, english tons per acre",
        required=False,
    )

    spring_c_to_n_ratio = forms.DecimalField(
        decimal_places=2,
        max_digits=5,
        label="Spring C to N ratio, agsource",
        required=False,
    )
    
    spring_percent_p = forms.DecimalField(
        decimal_places=2,
        max_digits=7,
        label="Spring Phosphorus content as percent of dry matter, agsource",
        required=False,
    )
    spring_percent_k = forms.DecimalField(
        decimal_places=2,
        max_digits=7,
        label="Spring Potassium content as percent of dry matter, agsource",
        required=False,
    )    
    spring_percent_ca = forms.DecimalField(
        decimal_places=2,
        max_digits=7,
        label="Spring Calcium content as percent of dry matter, agsource",
        required=False,
    )        
    spring_percent_mg = forms.DecimalField(
        decimal_places=2,
        max_digits=7,
        label="Spring Magnesium content as percent of dry matter, agsource",
        required=False,
    )         
    spring_percent_s = forms.DecimalField(
        decimal_places=2,
        max_digits=7,
        label="Spring Sulfur content as percent of dry matter, agsource",
        required=False,
    )               
    spring_p_content = forms.DecimalField(
        decimal_places=2,
        max_digits=7,
        label="Spring Phosphate (P2O5) content of forage if 100% dry matter, lbs/acre; agsource",
        required=False,
    )
    spring_n_content = forms.DecimalField(
        decimal_places=2,
        max_digits=7,
        label="Spring Nitrogen content of forage if 100% dry matter, lbs/acre; agsource",
        required=False,
    )    
    spring_k_content = forms.DecimalField(
        decimal_places=2,
        max_digits=7,
        label="Spring Potash (K2O) content of forage if 100% dry matter, lbs/acre; agsource",
        required=False,
    )    
    spring_ca_content = forms.DecimalField(
        decimal_places=2,
        max_digits=7,
        label="Spring Calcium content of forage if 100% dry matter, lbs/acre; agsource",
        required=False,
    )        
    spring_mg_content = forms.DecimalField(
        decimal_places=2,
        max_digits=7,
        label="Spring Magnesium content of forage if 100% dry matter, lbs/acre; agsource",
        required=False,
    )         
    spring_s_content = forms.DecimalField(
        decimal_places=2,
        max_digits=7,
        label="Spring Sulfur content of forage if 100% dry matter, lbs/acre; agsource",
        required=False,
    )
    spring_c_content = forms.DecimalField(
        decimal_places=2,
        max_digits=7,
        label="Spring Carbon content of forage if 100% dry matter, lbs/acre; agsource",
        required=False,
    )


    spring_acc_gdd = forms.DecimalField(
        decimal_places=2,
        max_digits=15,
        label="Spring Accumulated growing degree units",
        required=False,
    )
    spring_total_precip = forms.DecimalField(
        decimal_places=2,
        max_digits=15,
        label="Spring Total precipitation, in inches",
        required=False,
    )
    spring_rfq = forms.DecimalField(
        decimal_places=2,
        max_digits=15,
        label="Spring Relative forage quality (RFQ)",
        required=False,
    )

    spring_undfom240 = forms.DecimalField(
        decimal_places=2,
        max_digits=15,
        label="Spring uNDFOM240",
        required=False,
    )
    spring_dry_matter = forms.DecimalField(
        decimal_places=2,
        max_digits=15,
        label="Spring dry matter (%)",
        required=False,
    )
    spring_adf = forms.DecimalField(
        decimal_places=2,
        max_digits=15,
        label="Spring ADF (units?)",
        required=False,
    )
    spring_rfv = forms.DecimalField(
        decimal_places=2,
        max_digits=15,
        label="Spring Relative forage value (RFV)",
        required=False,
    )
    spring_cp = forms.DecimalField(
        decimal_places=2, max_digits=15, label="Spring Crude protein", required=False
    )
    spring_andf = forms.DecimalField(
        decimal_places=2, max_digits=15, label="Spring ANDF", required=False
    )
    spring_undfom30 = forms.DecimalField(
        decimal_places=2, max_digits=15, label="Spring undfom30", required=False
    )
    spring_ndfd30 = forms.DecimalField(
        decimal_places=2, max_digits=15, label="Spring ndfd30", required=False
    )
    spring_tdn_adf = forms.DecimalField(
        decimal_places=2, max_digits=15, label="Spring tdn_adf", required=False
    )
    spring_milk_ton_milk2013 = forms.DecimalField(
        decimal_places=2,
        max_digits=15,
        label="Spring milk per ton of feed",
        required=False,
    )
    spring_total_nitrogen = forms.DecimalField(
        decimal_places=2, max_digits=15, label="Spring Nitrogen content as percent of dry matter, agsource", required=False
    )
    spring_notes = forms.CharField(
        label="Text to be displayed regarding spring biomass sampling or lab processing.",
        required=False,
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=1000,
    )
    notes_admin = forms.CharField(
        label="Notes about lab data or sampling or about edits. These notes will not be displayed.",
        required=False,
        widget=forms.Textarea(attrs={"rows": 10}),
        max_length=1000,
    )

    precip_preplant_3_wk = forms.DecimalField(
        decimal_places=3,
        max_digits=15,
        label="Sum of precipitation 3 weeks until cover crop planting date",
        required=False
    )
    precip_preplant_2_wk = forms.DecimalField(
        decimal_places=3,
        max_digits=15,
        label="Sum of precipitation 2 weeks until cover crop planting date",
        required=False
    )
    precip_preplant_1_wk = forms.DecimalField(
        decimal_places=3,
        max_digits=15,
        label="Sum of precipitation 1 week until cover crop planting date",
        required=False
    )
    precip_postplant_1_wk = forms.DecimalField(
        decimal_places=3,
        max_digits=15,
        label="Sum of precipitation from cover crop planting date until 1 week later",
        required=False
    )    
    precip_postplant_2_wk = forms.DecimalField(
        decimal_places=3,
        max_digits=15,
        label="Sum of precipitation from cover crop planting date until 2 weeks later",
        required=False
    )    
    precip_postplant_3_wk = forms.DecimalField(
        decimal_places=3,
        max_digits=15,
        label="Sum of precipitation from cover crop planting date until 3 weeks later",
        required=False
    )            


    class Meta:
        model = AncillaryData
        fields = (
            "biomass_collection_date",
            "acc_gdd",
            "total_precip",
            "precip_preplant_3_wk",
            "precip_preplant_2_wk",
            "precip_preplant_1_wk",
            "precip_postplant_1_wk",
            "precip_postplant_2_wk",
            "precip_postplant_3_wk",
            "fall_notes",

            "cp",
            "andf",
            "undfom30",
            "ndfd30",
            "tdn_adf",
            "milk_ton_milk2013",
            "rfq",
            "undfom240",
            "dry_matter",
            "adf",
            "rfv",

            "cc_biomass",
            "total_nitrogen",
            "height_of_stand",
            "c_to_n_ratio",
            "percent_p",
            "percent_k",
            "percent_ca",
            "percent_mg",
            "percent_s",
            "p_content",
            "n_content",
            "k_content",
            "ca_content",
            "mg_content",
            "c_content",
    


            "spring_biomass_collection_date",
            
            "spring_cc_biomass",
            "spring_height_of_stand",

            "spring_rfq",
            "spring_undfom240",
            "spring_dry_matter",
            "spring_adf",
            "spring_rfv",
            "spring_acc_gdd",
            "spring_total_precip",
            "spring_cp",
            "spring_andf",
            "spring_undfom30",
            "spring_ndfd30",
            "spring_tdn_adf",
            "spring_milk_ton_milk2013",
            "spring_total_nitrogen",

            "spring_c_to_n_ratio",
            "spring_percent_p",
            "spring_percent_k",
            "spring_percent_ca",
            "spring_percent_mg",
            "spring_percent_s",
            "spring_p_content",
            "spring_n_content",
            "spring_k_content",
            "spring_ca_content",
            "spring_mg_content",
            "spring_c_content",

            "spring_notes",
            "notes_admin",
        )


class SelectUserForm(forms.Form):
    users = User.objects.filter(is_active=True)
    # user_select = forms.ModelMultipleChoiceField(queryset=users, to_field_name="email")
    user_select = forms.ChoiceField(choices=users.values_list("id", "email"))

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields["user_select"].queryset = User.objects.all()


class InterestedPartyForm(forms.ModelForm):
    first_name = forms.CharField(label="First name", max_length=250, required=True)
    last_name = forms.CharField(label="Last name", max_length=250, required=True)
    email = forms.EmailField(required=True)
    cover_crops_interest = forms.CharField(
        label="What is your interest in cover crops? What are your biggest questions?",
        widget=forms.Textarea(attrs={"rows": 10}),
        max_length=1000,
        required=False,
    )
    admin_notes = forms.CharField(
        label="Notes about interested party",
        required=False,
        widget=forms.Textarea(attrs={"rows": 10}),
        max_length=500,
    )

    class Meta:
        model = InterestedParty
        fields = (
            "first_name",
            "last_name",
            "email",
            "cover_crops_interest",
            "admin_notes",
        )


class InterestedAgronomistForm(forms.ModelForm):
    first_name = forms.CharField(label="First name", max_length=250, required=True)
    last_name = forms.CharField(label="Last name", max_length=250, required=True)
    email = forms.EmailField(label="Email", required=True)
    phone_number = forms.CharField(label="Phone number", max_length=250, required=True)
    affiliation = forms.CharField(
        label="Affiliation",
        required=True,
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=250,
    )
    location_area_of_work = forms.CharField(
        label="What is your location or area of work?",
        required=True,
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=500,
    )
    questions_for_us = forms.CharField(
        label="Do you have any questions for us?",
        widget=forms.Textarea(attrs={"rows": 10}),
        max_length=1000,
        required=False,
    )
    availability = forms.ChoiceField(
        label="Choose one or more option below:",
        widget=forms.RadioSelect,
        choices=InterestedAgronomist.AvailabilityChoices.choices,
        required=True,
    )
    admin_notes = forms.CharField(
        label="Notes about interested party",
        required=False,
        widget=forms.Textarea(attrs={"rows": 10}),
        max_length=500,
    )

    class Meta:
        model = InterestedAgronomist
        fields = (
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "affiliation",
            "location_area_of_work",
            "questions_for_us",
            "availability",
            "admin_notes",
        )
