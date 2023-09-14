from django import forms
from django.contrib.gis import forms as geo_forms
from wisccc.models import Survey, Farmer
from wisccc.models import (
    CashCropChoices,
    CoverCropChoices,
    CoverCropInfoSourcesChoices,
    CoverCropSupportChoices,
    CoverCropReasonsChoices,
    ManureApplicateUnitsChoices,
    NutrientMgmtSourcesChoices,
    PrimaryTillageEquipmentChoices,
    SecondaryTillageEquipmentChoices,
    SeedingMethodChoices,
    SoilConditionsSeedingChoices,
    SoilTextureClassChoices,
    TerminationMethodTimingChoices,
    TillageSystemChoices,
    CoverCropRateUnitsChoices,
)

TRUE_FALSE_CHOICES = ((True, "Yes"), (False, "No"))


class FarmerForm(forms.ModelForm):
    first_name = forms.CharField(max_length=250, required=True)
    last_name = forms.CharField(max_length=250, required=True)
    farm_name = forms.CharField(max_length=250, required=False)
    county = forms.CharField(
        max_length=500,
        label="In what county do you farm? (If you farm in more than one, list them in order of number of acres.) ",
        required=True,
        widget=forms.Textarea,
    )

    class Meta:
        model = Farmer
        fields = ("first_name", "last_name", "farm_name", "county")


class SurveyForm1(forms.ModelForm):
    # 2. Years Experience
    years_experience = forms.IntegerField(
        label="How many total years experience do you have planting cover crops?",
        required=True,
        min_value=0,
        max_value=100,
    )

    # 3. Total acres of cover crops
    total_acres = forms.IntegerField(
        label="Total acres you planted to cover crops this year.",
        required=True,
        min_value=0,
        max_value=100000,
    )

    # 4. Percent acres of your farm in cc?
    percent_of_farm_cc = forms.IntegerField(
        label="What percent of all your farm acres did you plant to covers this year?",
        required=True,
        min_value=0,
        max_value=100000,
    )
    # 5. Do you know the dominant soil series on your farm? If so, please list them below in order of how widely distributed (ex. Plano silt loam).
    dominant_soil_series_1 = forms.CharField(
        label="If you know the dominant soil series on your farm please list them below in order of how widely distributed. (ex. Plano, Drummer, Tama).",
        help_text="Most dominant",
        max_length=50,
        required=True,
    )

    dominant_soil_series_2 = forms.CharField(
        label="",
        help_text="Second most dominant",
        max_length=50,
        required=False,
    )
    dominant_soil_series_3 = forms.CharField(
        label="",
        help_text="Third most dominant",
        max_length=50,
        required=False,
    )
    dominant_soil_series_4 = forms.CharField(
        label="",
        help_text="Fourth most dominant",
        max_length=50,
        required=False,
    )

    # 6. From the following list, select and rank your top 1 - 3 sources of information for nutrient management:
    info_source_nutrient_mgmt_1 = forms.ChoiceField(
        label="What are your top three sources of information for nutrient management?",
        help_text="First",
        choices=NutrientMgmtSourcesChoices.choices,
        required=True,
    )
    info_source_nutrient_mgmt_2 = forms.ChoiceField(
        label="",
        help_text="Second",
        choices=NutrientMgmtSourcesChoices.choices,
        required=False,
    )
    info_source_nutrient_mgmt_3 = forms.ChoiceField(
        label="",
        help_text="Third",
        choices=NutrientMgmtSourcesChoices.choices,
        required=False,
    )

    source_nutrient_mgmt_write_in = forms.CharField(
        label='If you chose "other" please explain.',
        required=False,
        widget=forms.Textarea,
        max_length=500,
    )

    # 6a. For using cover crops for nutrient management, do you have any experiences to share or questions you'd like more information on?
    cov_crops_for_ntrnt_mgmt_comments_questions = forms.CharField(
        label="For using cover crops for nutrient management, do you have any experiences to share or questions you'd like more information on?",
        required=True,
        widget=forms.Textarea,
        max_length=1000,
    )

    # 7. From the following list select and rank your top 1 - 3 most important sources of information on cover cropping:
    info_source_cover_crops_1 = forms.ChoiceField(
        label="What are your top three sources of information on cover cropping?",
        help_text="First",
        choices=CoverCropInfoSourcesChoices.choices,
        required=True,
    )

    info_source_cover_crops_2 = forms.ChoiceField(
        label="",
        help_text="Second",
        choices=CoverCropInfoSourcesChoices.choices,
        required=False,
    )

    info_source_cover_crops_3 = forms.ChoiceField(
        label="",
        help_text="Third",
        choices=CoverCropInfoSourcesChoices.choices,
        required=False,
    )

    info_source_cover_crops_write_in = forms.CharField(
        label="If you chose “social media” or “other” please provide details.",
        required=False,
        widget=forms.Textarea,
        max_length=500,
    )
    # 7a. If you selected social media, what people or programs are most useful to you on questions of cover cropping?
    info_source_cover_crops_social_media = forms.CharField(
        label="PROBABLY delte this: Social media information source for cover crops",
        required=True,
        widget=forms.Textarea,
        max_length=500,
    )

    # 8. In terms of support for cover cropping, select and rank the top 1 to 3 factors you’d like to see more of:
    support_cover_crops_1 = forms.ChoiceField(
        label="Which of the following would make the biggest difference to you in terms of support for using cover crops?",
        choices=CoverCropSupportChoices.choices,
        required=True,
    )

    # support_cover_crops_2 = forms.ChoiceField(
    #     label="Second most needed support for cover cropping",
    #     choices=CoverCropSupportChoices.choices,
    #     required=False,
    # )

    # support_cover_crops_3 = forms.ChoiceField(
    #     label="Third most needed support for cover cropping",
    #     choices=CoverCropSupportChoices.choices,
    #     required=False,
    # )

    support_cover_crops_write_in = forms.CharField(
        label="If you chose “other” please provide details.",
        required=False,
        widget=forms.Textarea,
        max_length=500,
    )

    # 9. Are you lacking in any information regarding your selecting, planting, and managing cover crops?
    lacking_any_info_cover_crops = forms.CharField(
        label="Are you lacking in any information regarding cover crops? Please explain.",
        required=True,
        widget=forms.Textarea,
        max_length=500,
    )
    # 10. Would you like to expand the number of acres you plant to cover crops?
    # like_to_expand_cover_crops = forms.BooleanField(
    #     label="Would you like to expand the number of cover crop acres?",
    #     required=False,
    # )
    # 10 b. If yes, what are the main barries to expansion?
    # Please share any details that will help us understand the challenges.
    barriers_to_expansion = forms.CharField(
        label="Would you like to expand the number of acres you cover crop? If yes, what are the main barriers? Please share any details that will help us understand the challenges.",
        required=True,
        widget=forms.Textarea,
        max_length=1000,
    )

    # 11. What are the top risks of cover cropping for you, and how do you manage them?
    top_risks_of_cover_cropping_mgmt = forms.CharField(
        label="What are the top risks of cover cropping for you, and how do you manage them?",
        required=True,
        widget=forms.Textarea,
        max_length=500,
    )
    # 11a. What would it take for you to quit planting covers?
    quit_planting_cover_crops = forms.CharField(
        label="What would it take for you to quit planting covers?",
        required=True,
        widget=forms.Textarea,
        max_length=500,
    )
    # 12. Do you use crop insurance?
    use_crop_insurance = forms.BooleanField(
        label="Do you use crop insurance?", required=False
    )
    # 12a. If so, does it influence your cover cropping decisions, and how?
    if_use_crop_insurance = forms.CharField(
        label="Do you use crop insurance? If so, does it influence your cover cropping decisions, and how?",
        required=True,
        widget=forms.Textarea,
        max_length=500,
    )
    # 13. Why do you cover crop? From the list below select and rank your top 3 - 5 motivations

    why_cover_crops_1 = forms.ChoiceField(
        label="Why do you use cover cropping?",
        choices=CoverCropReasonsChoices.choices,
        required=False,
    )
    why_cover_crops_2 = forms.ChoiceField(
        label="Second reason you use cover cropping?",
        choices=CoverCropReasonsChoices.choices,
        required=False,
    )
    why_cover_crops_3 = forms.ChoiceField(
        label="Third reason you use cover cropping?",
        choices=CoverCropReasonsChoices.choices,
        required=False,
    )
    why_cover_crops_4 = forms.ChoiceField(
        label="Fourth reason you use cover cropping?",
        choices=CoverCropReasonsChoices.choices,
        required=False,
    )
    why_cover_crops_write_in = forms.CharField(
        label="What are your top 3 motivations for cover cropping? Please explain.",
        help_text="Answers might include beneficial insects, disease and pest management, carbon sequestration, conservation program cost sharing, forage production, water quality, build organic matter, soil erosion, resilience/trafficability of fields, soil structure, weed suppression, other.",
        required=True,
        widget=forms.Textarea,
        max_length=500,
    )

    class Meta:
        model = Survey
        fields = (
            "years_experience",
            "total_acres",
            "percent_of_farm_cc",
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
            # "info_source_cover_crops_2",
            # "info_source_cover_crops_3",
            "info_source_cover_crops_write_in",
            # "info_source_cover_crops_social_media",
            "support_cover_crops_1",
            "support_cover_crops_2",
            "support_cover_crops_3",
            "support_cover_crops_write_in",
            "lacking_any_info_cover_crops",
            "like_to_expand_cover_crops",
            "barriers_to_expansion",
            "top_risks_of_cover_cropping_mgmt",
            "quit_planting_cover_crops",
            "use_crop_insurance",
            "if_use_crop_insurance",
            "why_cover_crops_1",
            "why_cover_crops_2",
            "why_cover_crops_3",
            "why_cover_crops_4",
            "why_cover_crops_write_in",
        )


class SurveyForm2(forms.ModelForm):
    """Second section: field specific info"""

    # In the following section we ask you about your specific cover cropping practices in one field or set of fields (can be one acre ro 1,000) from which you'll take your samples for biomass, nutrient, and forage analysis. Provide answers *for that field.*
    farm_location = geo_forms.PointField(
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
        label="Zoom in to the map and click the general location for this field",
        help_text="To reset the location, click 'Delete all features' and click a different location",
        widget=geo_forms.OSMWidget(
            attrs={
                # 'map_width': 650,
                # 'map_height': 500,
                "default_lat": 44.636774,
                "default_lon": -90.012530,
                "default_zoom": 6,
            }
        ),
        required=False,
    )
    # 16 Closest zip code for this field (so we can determine appropriate climate data and generate a location map of participating fields). Field must be located in Wisconsin.
    closest_zip_code = forms.IntegerField(
        label="Enter the closest zip code for this field.",
        required=True,
        min_value=0,
        max_value=99999,
    )
    # 17 What is this field(s) acreage?
    field_acreage = forms.IntegerField(
        label="What is this field's acreage?", required=True, min_value=0
    )
    # ??	Question about multiple year rotation?
    # 18	"Please describe your crop rotation for this field including cover crops.
    # 2021. Cash crop drop down        cover crop drop down
    # 2022 Cash crop drop down        cover crop drop down
    # 2023 Cash crop drop down        cover crop drop down
    crop_rotation = forms.CharField(
        label="Are there any other details you would like to share about your crop rotation?",
        widget=forms.Textarea,
        max_length=500,
        required=False,
    )
    # 18a.
    crop_rotation_2021_cover_crop_species = forms.ChoiceField(
        label="Cover crop planted in 2021",
        choices=CoverCropChoices.choices,
        required=True,
        initial=CoverCropChoices.BLANK,
    )

    crop_rotation_2021_cash_crop_species = forms.ChoiceField(
        label="Cash crop planted 2021",
        choices=CashCropChoices.choices,
        required=True,
        initial=CashCropChoices.BLANK,
    )
    # 18b.
    crop_rotation_2022_cover_crop_species = forms.ChoiceField(
        label="Cover crop planted in 2022",
        choices=CoverCropChoices.choices,
        required=True,
        initial=CoverCropChoices.BLANK,
    )

    crop_rotation_2022_cash_crop_species = forms.ChoiceField(
        label="Cash crop planted 2022",
        choices=CashCropChoices.choices,
        required=True,
    )
    # 18c.
    crop_rotation_2023_cover_crop_species = forms.ChoiceField(
        label="Cover crop in planted 2023",
        choices=CoverCropChoices.choices,
        required=True,
    )

    crop_rotation_2023_cash_crop_species = forms.ChoiceField(
        label="Cash crop planted 2023",
        choices=CashCropChoices.choices,
        required=True,
    )

    # 19	"Please select any of the following that were planted as a cover crop in this field *this year*.
    # 31	At what rate did you plant your cover crops (please type species and pounds per acre).

    # Species 1
    cover_crop_species_1 = forms.ChoiceField(
        label="Cover crop 1",
        choices=CoverCropChoices.choices,
        required=True,
    )
    cover_crop_planting_rate_1 = forms.IntegerField(
        label="Planting rate, for cover crop 1", required=True
    )
    cover_crop_planting_rate_1_units = forms.ChoiceField(
        label="Units for cover crop 1",
        choices=CoverCropRateUnitsChoices.choices,
        required=True,
    )
    # Species 2
    cover_crop_species_2 = forms.ChoiceField(
        label="Cover crop 2",
        choices=CoverCropChoices.choices,
        required=False,
    )
    cover_crop_planting_rate_2 = forms.IntegerField(
        label="Planting rate, for cover crop 2", required=False
    )
    cover_crop_planting_rate_2_units = forms.ChoiceField(
        label="Units for cover crop 2",
        choices=CoverCropRateUnitsChoices.choices,
        required=False,
    )
    # Species 3
    cover_crop_species_3 = forms.ChoiceField(
        label="Cover crop 3",
        choices=CoverCropChoices.choices,
        required=False,
    )
    cover_crop_planting_rate_3 = forms.IntegerField(
        label="Planting rate, for cover crop 3", required=False
    )
    cover_crop_planting_rate_3_units = forms.ChoiceField(
        label="Units for cover crop 3",
        choices=CoverCropRateUnitsChoices.choices,
        required=False,
    )
    # Species 4
    cover_crop_species_4 = forms.ChoiceField(
        label="Cover crop 4",
        choices=CoverCropChoices.choices,
        required=False,
    )
    cover_crop_planting_rate_4 = forms.IntegerField(
        label="Planting rate, for cover crop 4", required=False
    )
    cover_crop_planting_rate_4_units = forms.ChoiceField(
        label="Units for cover crop 4",
        choices=CoverCropRateUnitsChoices.choices,
        required=False,
    )
    # Species 5
    cover_crop_species_5 = forms.ChoiceField(
        label="Cover crop 5",
        choices=CoverCropChoices.choices,
        required=False,
    )
    cover_crop_planting_rate_5 = forms.IntegerField(
        label="Planting rate, for cover crop 5", required=False
    )
    cover_crop_planting_rate_5_units = forms.ChoiceField(
        label="Units for cover crop 5",
        choices=CoverCropRateUnitsChoices.choices,
        required=False,
    )

    cover_crop_species_and_rate_write_in = forms.CharField(
        label="Other cover crops planted and their rates, please specify in pounds per acre.",
        widget=forms.Textarea,
        max_length=500,
        required=False,
    )

    cover_crop_multispecies_mix_write_in = forms.CharField(
        label="If you planted a multispecies mix in 2023 please provide details.",
        widget=forms.Textarea,
        max_length=500,
        required=False,
    )

    # 20	"Previous crop in field
    # DELETED
    previous_crop = forms.ChoiceField(
        label="Previous cash crop planted in this field in 2023.",
        choices=CashCropChoices.choices,
        required=False,
    )
    # 21	What date this year did you plant your cash crop in this field?
    cash_crop_planting_date = forms.DateField(
        label="What date this year did you plant your cash crop in this field? (Estimate is OK if not known)",
        required=True,
    )
    # 22	How many years have you been planting cover crops *in this field*?
    years_with_cover_crops = forms.IntegerField(
        label="How many years have you been planting cover crops *in this field*?",
        required=True,
        min_value=0,
        max_value=100,
    )
    # 23	"Please choose the dominant soil texture of the field.
    dominant_soil_texture = forms.ChoiceField(
        label="Please select the dominant soil texture of this field.",
        choices=SoilTextureClassChoices.choices,
        required=True,
    )

    # 14. Does planting a cover crop delay when you would otherwise plant your cash crop?
    cover_crops_delay_cash_crop = forms.ChoiceField(
        label="Does planting a cover crop delay when you would otherwise plant your cash crop?",
        choices=TRUE_FALSE_CHOICES,
        required=False,
    )

    # 15a. Do you save cover crop seed?
    save_cover_crop_seed = forms.ChoiceField(
        label="Do you save cover crop seed?",
        required=False,
        choices=TRUE_FALSE_CHOICES,
    )
    # 15b. What is your source for cover crop seed?
    source_cover_crop_seed = forms.CharField(
        label="What is your cover crop seed source?",
        required=True,
        widget=forms.Textarea,
        max_length=500,
    )

    # 24	Will you apply manure prior to seeding cover crops on this field, and at what rate?
    manure_prior = forms.ChoiceField(
        label="Will you apply manure prior to seeding cover crops on this field?",
        required=False,
        choices=TRUE_FALSE_CHOICES,
    )
    # 24a
    manure_prior_rate = forms.IntegerField(
        label="At what rate will the manure be applied?",
        required=False,
        min_value=0,
    )
    manure_prior_rate_units = forms.ChoiceField(
        label="The units for the manure application rate",
        choices=ManureApplicateUnitsChoices.choices,
        required=False,
    )

    # 25	Will manure be applied to the field after the cover crop is established?
    manure_post = forms.ChoiceField(
        label="Will manure be applied to the field after the cover crop is established?",
        required=False,
        choices=TRUE_FALSE_CHOICES,
    )
    # 25a
    manure_post_rate = forms.IntegerField(
        label="At what rate will the manure be applied?",
        required=False,
        min_value=0,
    )
    manure_post_rate_units = forms.ChoiceField(
        label="The units for the manure application rate",
        choices=ManureApplicateUnitsChoices.choices,
        required=False,
    )
    # 26	"What is your tillage system for the cash crop preceding the cover crop?
    tillage_system_cash_crop = forms.ChoiceField(
        label="What is your tillage system for the cash crop preceding the cover crop?",
        choices=TillageSystemChoices.choices,
        required=True,
    )
    # 27	"Primary tillage equipment (select all that apply) for a cash crop preceding a cover crop?
    primary_tillage_equipment_1 = forms.ChoiceField(
        label="Primary tillage equipment (select all that apply) for a cash crop preceding a cover crop?",
        choices=PrimaryTillageEquipmentChoices.choices,
        required=True,
    )
    primary_tillage_equipment_2 = forms.ChoiceField(
        label="Primary tillage equipment",
        choices=PrimaryTillageEquipmentChoices.choices,
        required=False,
    )
    primary_tillage_equipment_write_in = forms.CharField(
        label="If you selected other, please explain.",
        widget=forms.Textarea,
        max_length=500,
        required=False,
    )
    # 28	"Secondary tillage equipment (select all that apply) for cash crop preceding the cover crop?
    secondary_tillage_equipment = forms.ChoiceField(
        label="Secondary tillage equipment (select all that apply) for cash crop preceding the cover crop?",
        choices=SecondaryTillageEquipmentChoices.choices,
        required=False,
    )
    secondary_tillage_equipment_write_in = forms.CharField(
        label="If you selected other, please explain.",
        widget=forms.Textarea,
        max_length=500,
        required=False,
    )

    # 29	"Soil conditions in this field at cover crop seeding
    soil_conditions_at_cover_crop_seeding = forms.ChoiceField(
        label="Soil conditions in this field at cover crop seeding.",
        choices=SoilConditionsSeedingChoices.choices,
        required=True,
    )

    # 30	"Cover Crop Seeding Method.
    cover_crop_seeding_method = forms.ChoiceField(
        label="Please select your the seeding method for your cover crop.",
        choices=SeedingMethodChoices.choices,
        required=True,
    )

    cover_crop_seeding_method_write_in = forms.CharField(
        label="If you selected other, please explain.",
        widget=forms.Textarea,
        max_length=500,
        required=False,
    )

    # 32
    cover_crop_seed_cost = forms.IntegerField(
        label="Estimated cover crop seed cost for this field ($/acre)",
        min_value=0,
        required=True,
    )
    # 33	Estimated cover crop planting cost per acre in this field. Please use UW Extension Custom Rate Guide.(https://www.nass.usda.gov/Statistics_by_State/Wisconsin/Publications/WI-CRate20.pdf)
    cover_crop_planting_cost = forms.IntegerField(
        label='Estimated cover crop planting cost per acre in this field. Please use <a href="https://www.nass.usda.gov/Statistics_by_State/Wisconsin/Publications/WI-CRate20.pdf">UW Extension Custom Rate Guide.</a>',
        min_value=0,
        required=True,
    )
    # 34	Cover crop planting date for this field (estimate is OK if not known).
    cover_crop_planting_date = forms.DateField(
        label="Cover crop planting date for this field (estimate is OK if not known).",
        required=True,
    )
    # 35	"Estimated termination timing/method for this field.
    cover_crop_estimated_termination = forms.ChoiceField(
        label="Estimated termination timing/method for this field.",
        choices=TerminationMethodTimingChoices.choices,
        required=True,
    )

    # 36	Number of days estimated between crop harvest and cover crop establishment in this field.
    days_between_crop_hvst_and_cc_estd = forms.IntegerField(
        label="Number of days estimated between crop harvest and cover crop establishment in this field.",
        min_value=0,
        max_value=365,
        required=True,
    )

    class Meta:
        model = Survey
        fields = (
            "farm_location",
            "closest_zip_code",
            "field_acreage",
            "crop_rotation",
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
            "cover_crop_species_and_rate_write_in",
            "previous_crop",
            "cash_crop_planting_date",
            "years_with_cover_crops",
            "dominant_soil_texture",
            "manure_prior",
            "manure_prior_rate",
            "manure_prior_rate_units",
            "manure_post",
            "manure_post_rate",
            "manure_post_rate_units",
            "tillage_system_cash_crop",
            "primary_tillage_equipment_1",
            # "primary_tillage_equipment_2",
            "primary_tillage_equipment_write_in",
            "secondary_tillage_equipment",
            "secondary_tillage_equipment_write_in",
            "soil_conditions_at_cover_crop_seeding",
            "cover_crop_seeding_method",
            "cover_crop_seeding_method_write_in",
            "cover_crop_seed_cost",
            "cover_crop_planting_cost",
            "cover_crop_planting_date",
            "cover_crop_estimated_termination",
            "days_between_crop_hvst_and_cc_estd",
            "cover_crops_delay_cash_crop",
            "save_cover_crop_seed",
            "source_cover_crop_seed",
        )


class SurveyForm3(forms.ModelForm):
    """Third section, final thoughts"""

    # 37	Please share any interesting experiments, failures, equipment challenges with cover crops.
    interesting_tales = forms.CharField(
        label="What has been your cover crop “learning curve”? Please share with any interesting experiments including failures that have helped you adapt cover cropping to your farm.",
        widget=forms.Textarea,
        max_length=1000,
        required=True,
    )
    # 38	If another grower asked you where to start with cover cropping what would you recommend and why?
    where_to_start = forms.CharField(
        label="Where would you tell another grower to start with cover crops? Why?",
        widget=forms.Textarea,
        max_length=1000,
        required=True,
    )
    # 39	Do you have any additional thoughts or questions about this data gathering process? Any important survey questions we should ask next time?
    additional_thoughts = forms.CharField(
        label="Any additional thoughts or questions? Any important survey questions we should ask next time?",
        widget=forms.Textarea,
        max_length=1000,
        required=True,
    )

    class Meta:
        model = Survey
        fields = (
            "interesting_tales",
            "where_to_start",
            "additional_thoughts",
        )


class SurveyForm(forms.ModelForm):
    # county = forms.CharField(
    #     label="County",
    #     help_text="Enter the county of this field.",
    #     required=True,
    # )

    # 2. Years Experience
    years_experience = forms.IntegerField(
        label="Years experience of farming", required=True, min_value=0, max_value=100
    )

    # 3. Total acres of cover crops
    total_acres = forms.IntegerField(
        label="Total acres of cover crops",
        required=True,
        min_value=0,
        max_value=100000,
    )

    # 4. Percent acres of your farm in cc?
    percent_of_farm_cc = forms.IntegerField(
        label="The percent of your farm, in acres, that is planted in cover crops",
        required=True,
        min_value=0,
        max_value=100000,
    )
    # 5. Do you know the dominant soil series on your farm? If so, please list them below in order of how widely distributed (ex. Plano silt loam).
    dominant_soil_series_1 = forms.CharField(
        label="Soil series with the greatest distribution on your farm",
        help_text="Soil series with the greatest distribution on your farm",
        max_length=50,
        required=True,
    )

    dominant_soil_series_2 = forms.CharField(
        label="Soil series with the second greatest distribution on your farm",
        max_length=50,
        required=True,
    )
    dominant_soil_series_3 = forms.CharField(
        label="Soil series with the third greatest distribution on your farm",
        max_length=50,
        required=True,
    )
    dominant_soil_series_4 = forms.CharField(
        label="Soil series with the fourth greatest distribution on your farm",
        max_length=50,
        required=True,
    )

    # 6. From the following list, select and rank your top 1 - 3 sources of information for nutrient management:
    info_source_nutrient_mgmt_1 = forms.ChoiceField(
        label="Top information source for nutrient management",
        choices=NutrientMgmtSourcesChoices.choices,
        required=True,
    )
    info_source_nutrient_mgmt_2 = forms.ChoiceField(
        label="Second information source for nutrient management",
        choices=NutrientMgmtSourcesChoices.choices,
        required=True,
    )
    info_source_nutrient_mgmt_3 = forms.ChoiceField(
        label="Third information source for nutrient management",
        choices=NutrientMgmtSourcesChoices.choices,
        required=True,
    )

    source_nutrient_mgmt_write_in = forms.CharField(
        label="Other information source for nutrient management?",
        required=False,
        widget=forms.Textarea,
        max_length=500,
    )

    # 6a. For using cover crops for nutrient management, do you have any experiences to share or questions you'd like more information on?
    cov_crops_for_ntrnt_mgmt_comments_questions = forms.CharField(
        label="Questions or comments about nutrient management and cover crops",
        required=True,
        widget=forms.Textarea,
        max_length=1000,
    )

    # 7. From the following list select and rank your top 1 - 3 most important sources of information on cover cropping:
    info_source_cover_crops_1 = forms.ChoiceField(
        label="Top information source for cover crops",
        choices=CoverCropInfoSourcesChoices.choices,
        required=True,
    )

    info_source_cover_crops_2 = forms.ChoiceField(
        label="Second information source for cover crops",
        choices=CoverCropInfoSourcesChoices.choices,
        required=True,
    )

    info_source_cover_crops_3 = forms.ChoiceField(
        label="Third information source for cover crops",
        choices=CoverCropInfoSourcesChoices.choices,
        required=True,
    )

    info_source_cover_crops_write_in = forms.CharField(
        label="Other information source for cover crops",
        required=False,
        widget=forms.Textarea,
        max_length=500,
    )
    # 7a. If you selected social media, what people or programs are most useful to you on questions of cover cropping?
    info_source_cover_crops_social_media = forms.CharField(
        label="Social media information source for cover crops",
        required=True,
        widget=forms.Textarea,
        max_length=500,
    )

    # 8. In terms of support for cover cropping, select and rank the top 1 to 3 factors you’d like to see more of:
    support_cover_crops_1 = forms.ChoiceField(
        label="Most needed support for cover cropping",
        choices=CoverCropSupportChoices.choices,
        required=True,
    )

    # support_cover_crops_2 = forms.ChoiceField(
    #     label="Second most needed support for cover cropping",
    #     choices=CoverCropSupportChoices.choices,
    #     required=False,
    # )

    # support_cover_crops_3 = forms.ChoiceField(
    #     label="Third most needed support for cover cropping",
    #     choices=CoverCropSupportChoices.choices,
    #     required=False,
    # )

    support_cover_crops_write_in = forms.CharField(
        label="Other support for cover crops you would like to see",
        required=True,
        widget=forms.Textarea,
        max_length=500,
    )

    # 9. Are you lacking in any information regarding your selecting, planting, and managing cover crops?
    lacking_any_info_cover_crops = forms.CharField(
        label="Are you lacking in any information regarding cover crops?",
        required=True,
        widget=forms.Textarea,
        max_length=500,
    )
    # 10. Would you like to expand the number of acres you plant to cover crops?
    like_to_expand_cover_crops = forms.BooleanField(
        label="Would you like to expand the number of cover crop acres?",
        required=False,
    )
    # 10 b. If yes, what are the main barries to expansion?
    # Please share any details that will help us understand the challenges.
    barriers_to_expansion = forms.CharField(
        label="What are your barriers to expansion? Please share any details to help us understand.",
        required=True,
        widget=forms.Textarea,
        max_length=1000,
    )

    # 11. What are the top risks of cover cropping for you, and how do you manage them?
    top_risks_of_cover_cropping_mgmt = forms.CharField(
        label="What are the top risks of cover cropping for you, and how do you manage them?",
        required=False,
        widget=forms.Textarea,
        max_length=500,
    )
    # 11a. What would it take for you to quit planting covers?
    quit_planting_cover_crops = forms.CharField(
        label="What would it take for you to quit planting covers?",
        required=True,
        widget=forms.Textarea,
        max_length=500,
    )
    # 12. Do you use crop insurance?
    use_crop_insurance = forms.BooleanField(
        label="Do you use crop insurance?", required=False
    )
    # 12a. If so, does it influence your cover cropping decisions, and how?
    if_use_crop_insurance = forms.CharField(
        label="If so, does it influence your cover cropping decisions, and how?",
        required=False,
        widget=forms.Textarea,
        max_length=500,
    )
    # 13. Why do you cover crop? From the list below select and rank your top 3 - 5 motivations

    why_cover_crops_1 = forms.ChoiceField(
        label="Why do you use cover cropping?",
        choices=CoverCropReasonsChoices.choices,
        required=True,
    )
    why_cover_crops_2 = forms.ChoiceField(
        label="Second reason you use cover cropping?",
        choices=CoverCropReasonsChoices.choices,
        required=False,
    )
    why_cover_crops_3 = forms.ChoiceField(
        label="Third reason you use cover cropping?",
        choices=CoverCropReasonsChoices.choices,
        required=False,
    )
    why_cover_crops_4 = forms.ChoiceField(
        label="Fourth reason you use cover cropping?",
        choices=CoverCropReasonsChoices.choices,
        required=False,
    )
    why_cover_crops_write_in = forms.CharField(
        label="Other reasons you plant cover crops?",
        required=False,
        widget=forms.Textarea,
        max_length=500,
    )
    # 14. Does planting a cover crop delay when you would otherwise plant your cash crop?
    cover_crops_delay_cash_crop = forms.BooleanField(
        label="Does planting a cover crop delay when you would otherwise plant your cash crop?",
        required=False,
    )

    # 15a. Do you save cover crop seed?
    save_cover_crop_seed = forms.BooleanField(
        label="Do you save cover crop seed?", required=False
    )
    # 15b. What is your source for cover crop seed?
    source_cover_crop_seed = forms.CharField(
        label="What is your cover crop seed source?",
        required=True,
        widget=forms.Textarea,
        max_length=500,
    )

    # In the following section we ask you about your specific cover cropping practices in one field or set of fields (can be one acre or 1,000) from which you'll take your samples for biomass, nutrient, and forage analysis. Provide answers *for that field.*
    farm_location = geo_forms.PointField(
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
        label="Click the map where this field is located",
        help_text="To reset the location, click 'Delete all features' and click a different location",
        widget=geo_forms.OSMWidget(
            attrs={
                # 'map_width': 650,
                # 'map_height': 500,
                "default_lat": 44.636774,
                "default_lon": -90.012530,
                "default_zoom": 6,
            }
        ),
    )
    # 16 Closest zip code for this field (so we can determine appropriate climate data and generate a location map of participating fields). Field must be located in Wisconsin.
    closest_zip_code = forms.IntegerField(
        label="Enter the closest zip code for this field.", required=True
    )
    # 17 What is this field(s) acreage?
    field_acreage = forms.IntegerField(
        label="What is this field's acreage?", required=True, min_value=0
    )
    # ??	Question about multiple year rotation?
    # 18	"Please describe your crop rotation for this field including cover crops.
    # 2021. Cash crop drop down        cover crop drop down
    # 2022 Cash crop drop down        cover crop drop down
    # 2023 Cash crop drop down        cover crop drop down
    crop_rotation = forms.CharField(
        label="Please describe your crop rotation for this field, including cover crops.",
        widget=forms.Textarea,
        max_length=500,
    )
    # 18a.
    # GOOD CANDIDATE FOR MULTIPLE SELECT
    crop_rotation_2021_cover_crop_species = forms.ChoiceField(
        label="Cover crop species planted in 2021",
        choices=CoverCropChoices.choices,
        required=True,
    )

    crop_rotation_2021_cash_crop_species = forms.ChoiceField(
        label="Cash crop species planted 2021",
        choices=CashCropChoices.choices,
        required=True,
    )
    # 18b.
    crop_rotation_2022_cover_crop_species = forms.ChoiceField(
        label="Cover crop species planted in 2022",
        choices=CoverCropChoices.choices,
        required=True,
    )

    crop_rotation_2022_cash_crop_species = forms.ChoiceField(
        label="Cash crop species planted 2022",
        choices=CashCropChoices.choices,
        required=True,
    )
    # 18c.
    crop_rotation_2023_cover_crop_species = forms.ChoiceField(
        label="Cover crop species in planted 2023",
        choices=CoverCropChoices.choices,
        required=True,
    )

    crop_rotation_2023_cash_crop_species = forms.ChoiceField(
        label="Cash crop species planted 2023",
        choices=CashCropChoices.choices,
        required=True,
    )

    # 19	"Please select any of the following that were planted as a cover crop in this field *this year*.
    # 31	At what rate did you plant your cover crops (please type species and pounds per acre).

    # Species 1
    cover_crop_species_1 = forms.ChoiceField(
        label="Cover crop species 1",
        choices=CoverCropChoices.choices,
        required=True,
    )
    cover_crop_planting_rate_1 = forms.IntegerField(
        label="Cover crop planting rate, for species 1", required=True
    )

    # Species 2
    cover_crop_species_2 = forms.ChoiceField(
        label="Cover crop species 2",
        choices=CoverCropChoices.choices,
        required=False,
    )
    cover_crop_planting_rate_2 = forms.IntegerField(
        label="Cover crop planting rate, for species 2", required=False
    )
    # Species 3
    cover_crop_species_3 = forms.ChoiceField(
        label="Cover crop species 3",
        choices=CoverCropChoices.choices,
        required=False,
    )
    cover_crop_planting_rate_3 = forms.IntegerField(
        label="Cover crop planting rate, for species 3", required=False
    )
    # Species 4
    cover_crop_species_4 = forms.ChoiceField(
        label="Cover crop species 4",
        choices=CoverCropChoices.choices,
        required=False,
    )
    cover_crop_planting_rate_4 = forms.IntegerField(
        label="Cover crop planting rate, for species 4", required=False
    )
    # Species 5
    cover_crop_species_5 = forms.ChoiceField(
        label="Cover crop species 5",
        choices=CoverCropChoices.choices,
        required=False,
    )
    cover_crop_planting_rate_5 = forms.IntegerField(
        label="Cover crop planting rate, for species 5", required=False
    )

    cover_crop_species_and_rate_write_in = forms.CharField(
        label="Other cover crops planted and their rates, please specify in pounds per acre.",
        widget=forms.Textarea,
        max_length=500,
    )
    # 20	"Previous crop in field
    previous_crop = forms.ChoiceField(
        label="Previous cash crop planted in the field",
        choices=CashCropChoices.choices,
        required=True,
    )
    # 21	What date this year did you plant your cash crop in this field?
    cash_crop_planting_date = forms.DateField(
        label="What date this year did you plant your cash crop in this field?",
        required=True,
    )
    # 22	How many years have you been planting cover crops *in this field*?
    years_with_cover_crops = forms.IntegerField(
        label="How many years have you been planting cover crops *in this field*?",
        required=True,
        min_value=0,
        max_value=100,
    )
    # 23	"Please choose the dominant soil texture of the field.
    dominant_soil_texture = forms.ChoiceField(
        label="Please select the dominant soil texture of this field.",
        choices=SoilTextureClassChoices.choices,
        required=True,
    )

    # 24	Will you apply manure prior to seeding cover crops on this field, and at what rate?
    manure_prior = forms.BooleanField(
        label="Will you apply manure prior to seeding cover crops on this field?",
        required=False,
    )
    # 24a
    manure_prior_rate = forms.IntegerField(
        label="At what rate will the manure be applied?",
        required=False,
        min_value=0,
    )
    manure_prior_rate_units = forms.ChoiceField(
        label="The units for the manure application rate",
        choices=ManureApplicateUnitsChoices.choices,
        required=False,
    )

    # 25	Will manure be applied to the field after the cover crop is established?
    manure_post = forms.BooleanField(
        label="Will manure be applied to the field after the cover crop is established?",
        required=False,
    )
    # 25a
    manure_post_rate = forms.IntegerField(
        label="At what rate will the manure be applied?",
        required=False,
        min_value=0,
    )
    manure_post_rate_units = forms.ChoiceField(
        label="The units for the manure application rate",
        choices=ManureApplicateUnitsChoices.choices,
        required=False,
    )
    # 26	"What is your tillage system for the cash crop preceding the cover crop?
    tillage_system_cash_crop = forms.ChoiceField(
        label="Tillage system for cash crop preceding",
        choices=TillageSystemChoices.choices,
        required=True,
    )
    # 27	"Primary tillage equipment (select all that apply) for a cash crop preceding a cover crop?
    primary_tillage_equipment_1 = forms.ChoiceField(
        label="Primary tillage equipment",
        choices=PrimaryTillageEquipmentChoices.choices,
        required=False,
    )
    primary_tillage_equipment_2 = forms.ChoiceField(
        label="Primary tillage equipment",
        choices=PrimaryTillageEquipmentChoices.choices,
        required=False,
    )
    primary_tillage_equipment_write_in = forms.CharField(
        label="Primary tillage equipment, write in",
        widget=forms.Textarea,
        max_length=500,
        required=False,
    )
    # 28	"Secondary tillage equipment (select all that apply) for cash crop preceding the cover crop?
    secondary_tillage_equipment = forms.ChoiceField(
        label="Secondary tillage equipment",
        choices=SecondaryTillageEquipmentChoices.choices,
        required=False,
    )
    secondary_tillage_equipment_write_in = forms.CharField(
        label="Secondary tillage equipment, write in",
        widget=forms.Textarea,
        max_length=500,
        required=False,
    )

    # 29	"Soil conditions in this field at cover crop seeding
    soil_conditions_at_cover_crop_seeding = forms.ChoiceField(
        label="Soil conditions in this field at cover crop seeding",
        choices=SoilConditionsSeedingChoices.choices,
        required=True,
    )

    # 30	"Cover Crop Seeding Method.
    cover_crop_seeding_method = forms.ChoiceField(
        label="Cover crop seeding method",
        choices=SeedingMethodChoices.choices,
        required=True,
    )

    cover_crop_seeding_method_write_in = forms.CharField(
        label="Cover crop seeding method, write in",
        widget=forms.Textarea,
        max_length=500,
        required=False,
    )

    # 32
    cover_crop_seed_cost = forms.IntegerField(
        label="Estimated cover crop seed cost for this field ($/acre)",
        min_value=0,
        required=True,
    )
    # 33	Estimated cover crop planting cost per acre in this field. Please use UW Extension Custom Rate Guide.(https://www.nass.usda.gov/Statistics_by_State/Wisconsin/Publications/WI-CRate20.pdf)
    cover_crop_planting_cost = forms.IntegerField(
        label="Estimated cover crop planting cost for this field ($/acre)",
        min_value=0,
        required=True,
    )
    # 34	Cover crop planting date for this field (estimate is OK if not known).
    cover_crop_planting_date = forms.DateField(
        label="Estimated cover crop planting date", required=True
    )
    # 35	"Estimated termination timing/method for this field.
    cover_crop_estimated_termination = forms.ChoiceField(
        label="Estimated termination timing/method for this field.",
        choices=TerminationMethodTimingChoices.choices,
        required=True,
    )

    # 36	Number of days estimated between crop harvest and cover crop establishment in this field.
    days_between_crop_hvst_and_cc_estd = forms.IntegerField(
        label="Number of days estimated between crop harvest and cover crop establishment in this field.",
        min_value=0,
        max_value=365,
        required=True,
    )
    # 37	Please share any interesting experiments, failures, equipment challenges with cover crops.
    interesting_tales = forms.CharField(
        label="Interesting experiments, failures, equipment challenges",
        widget=forms.Textarea,
        max_length=1000,
        required=False,
    )
    # 38	If another grower asked you where to start with cover cropping what would you recommend and why?
    where_to_start = forms.CharField(
        label="Where would you tell another grower to start with cover crops? Why?",
        widget=forms.Textarea,
        max_length=1000,
        required=False,
    )
    # 39	Do you have any additional thoughts or questions about this data gathering process? Any important survey questions we should ask next time?
    additional_thoughts = forms.CharField(
        label="Any additional thoughts?",
        widget=forms.Textarea,
        max_length=1000,
        required=False,
    )

    class Meta:
        model = Survey
        fields = (
            "farm_location",
            "years_experience",
            "total_acres",
            "percent_of_farm_cc",
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
            "info_source_cover_crops_social_media",
            "support_cover_crops_1",
            "support_cover_crops_2",
            "support_cover_crops_3",
            "support_cover_crops_write_in",
            "lacking_any_info_cover_crops",
            "like_to_expand_cover_crops",
            "barriers_to_expansion",
            "top_risks_of_cover_cropping_mgmt",
            "quit_planting_cover_crops",
            "use_crop_insurance",
            "if_use_crop_insurance",
            "why_cover_crops_1",
            "why_cover_crops_2",
            "why_cover_crops_3",
            "why_cover_crops_4",
            "why_cover_crops_write_in",
            "cover_crops_delay_cash_crop",
            "save_cover_crop_seed",
            "source_cover_crop_seed",
            "closest_zip_code",
            "field_acreage",
            "crop_rotation",
            "crop_rotation_2021_cover_crop_species",
            "crop_rotation_2021_cash_crop_species",
            "crop_rotation_2022_cover_crop_species",
            "crop_rotation_2022_cash_crop_species",
            "crop_rotation_2023_cover_crop_species",
            "crop_rotation_2023_cash_crop_species",
            "cover_crop_species_1",
            "cover_crop_planting_rate_1",
            "cover_crop_species_2",
            "cover_crop_planting_rate_2",
            "cover_crop_species_3",
            "cover_crop_planting_rate_3",
            "cover_crop_species_4",
            "cover_crop_planting_rate_4",
            "cover_crop_species_5",
            "cover_crop_planting_rate_5",
            "cover_crop_species_and_rate_write_in",
            "previous_crop",
            "cash_crop_planting_date",
            "years_with_cover_crops",
            "dominant_soil_texture",
            "manure_prior",
            "manure_prior_rate",
            "manure_prior_rate_units",
            "manure_post",
            "manure_post_rate",
            "manure_post_rate_units",
            "tillage_system_cash_crop",
            "primary_tillage_equipment_1",
            "primary_tillage_equipment_2",
            "primary_tillage_equipment_write_in",
            "secondary_tillage_equipment",
            "secondary_tillage_equipment_write_in",
            "soil_conditions_at_cover_crop_seeding",
            "cover_crop_seeding_method",
            "cover_crop_seeding_method_write_in",
            "cover_crop_seed_cost",
            "cover_crop_planting_cost",
            "cover_crop_planting_date",
            "cover_crop_estimated_termination",
            "days_between_crop_hvst_and_cc_estd",
            "interesting_tales",
            "where_to_start",
            "additional_thoughts",
        )
