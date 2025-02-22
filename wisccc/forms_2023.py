from django import forms
from django.contrib.gis import forms as geo_forms

from django import forms
from wisccc.models import (
    SurveyFarm,
    SurveyField,
    FieldFarm,
)
from wisccc.models import (
    CashCropChoices,
    CoverCropChoices,
    CoverCropChoicesWMulti,
    CoverCropInfoSourcesChoices,
    CoverCropSupportChoices,
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

TRUE_FALSE_CHOICES = (("", ""), (True, "Yes"), (False, "No"))


"""Review forms are used when admin is reviewing, no required fields"""


class SurveyFarmFormPart1_2023(forms.ModelForm):

    # 1. Years Experience
    years_experience = forms.IntegerField(
        label="1. How many total years experience do you have planting cover crops?",
        required=True,
        min_value=0,
        max_value=100,
    )

    # 2. Total acres of cover crops
    total_acres = forms.IntegerField(
        label="2. Total acres you planted to cover crops this year.",
        required=True,
        min_value=0,
        max_value=100000,
    )

    # 3. Percent acres of your farm in cc?
    percent_of_farm_cc = forms.IntegerField(
        label="3. What percent of all your farm acres did you plant to covers this year?",
        required=True,
        min_value=0,
        max_value=100,
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
    info_source_cover_crops_1 = forms.ChoiceField(
        label="8. What are your top three sources of information on cover cropping?",
        help_text="First",
        choices=CoverCropInfoSourcesChoices.choices,
        required=True,
    )

    info_source_cover_crops_2 = forms.ChoiceField(
        label="",
        help_text="Second",
        choices=CoverCropInfoSourcesChoices.choices,
        required=True,
    )

    info_source_cover_crops_3 = forms.ChoiceField(
        label="",
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

    barriers_to_expansion = forms.CharField(
        label="13. Would you like to expand the number of acres you cover crop? If yes, what are the main barriers? Please share any details that will help us understand the challenges.",
        required=True,
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

    class Meta:
        model = SurveyFarm
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
            "info_source_cover_crops_2",
            "info_source_cover_crops_3",
            "info_source_cover_crops_write_in",
            "support_cover_crops_1",
            "support_cover_crops_write_in",
            "lacking_any_info_cover_crops",
            "barriers_to_expansion",
            "quit_planting_cover_crops",
            "if_use_crop_insurance",
            "why_cover_crops_write_in",
        )


class SurveyFarmFormPart2_2023(forms.ModelForm):

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

    class Meta:
        model = SurveyFarm
        fields = (
            "cover_crops_delay_cash_crop",
            "save_cover_crop_seed",
            "source_cover_crop_seed",
        )


class SurveyFarmFormPart3_2023(forms.ModelForm):

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

    class Meta:
        model = SurveyFarm
        fields = (
            "interesting_tales",
            "where_to_start",
            "additional_thoughts",
        )


class FieldFarmFormFull_2023(forms.ModelForm):
    """For static data about a farmer's field"""

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
            "closest_zip_code",
            "field_acreage",
            "field_location",
        )


class SurveyFieldFormFull_2023_parta(forms.ModelForm):

    # In the following section we ask you about your specific cover cropping practices in one field or set of fields (can be one acre ro 1,000) from which you'll take your samples for biomass, nutrient, and forage analysis. Provide answers *for that field.*
    # ??	Question about multiple year rotation?
    # 18	"Please describe your crop rotation for this field including cover crops.
    # 2021. Cash crop drop down        cover crop drop down
    # 2022 Cash crop drop down        cover crop drop down
    # 2023 Cash crop drop down        cover crop drop down
    # 20 a
    crop_rotation_2021_cash_crop_species = forms.ChoiceField(
        label="20a. Cash crop planted 2021",
        choices=CashCropChoices.choices,
        required=True,
        initial=CashCropChoices.BLANK,
    )
    # 20 b
    crop_rotation_2021_cover_crop_species = forms.ChoiceField(
        label="20b. Cover crop planted in 2021",
        choices=CoverCropChoicesWMulti.choices,
        required=True,
        initial=CoverCropChoices.BLANK,
    )

    # 21 a.
    crop_rotation_2022_cash_crop_species = forms.ChoiceField(
        label="21a. Cash crop planted 2022",
        choices=CashCropChoices.choices,
        required=True,
    )
    # 21 b
    crop_rotation_2022_cover_crop_species = forms.ChoiceField(
        label="21b. Cover crop planted in 2022",
        choices=CoverCropChoicesWMulti.choices,
        required=True,
        initial=CoverCropChoices.BLANK,
    )
    # 22 a.
    crop_rotation_2023_cash_crop_species = forms.ChoiceField(
        label="22a. Cash crop planted 2023",
        choices=CashCropChoices.choices,
        required=True,
    )
    # 22 b.
    crop_rotation_2023_cover_crop_species = forms.ChoiceField(
        label="22b. Cover crop in planted 2023",
        choices=CoverCropChoicesWMulti.choices,
        required=True,
    )
    # 23	"Please describe your crop rotation for this field including cover crops.
    crop_rotation = forms.CharField(
        label="23. Are there any other details you would like to share about your crop rotation?",
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=500,
        required=False,
    )

    # 24 a
    # Species 1
    cover_crop_species_1 = forms.ChoiceField(
        label="24. Cover crop 1",
        choices=CoverCropChoices.choices,
        required=True,
    )
    # 24b
    cover_crop_planting_rate_1 = forms.IntegerField(
        label="Planting rate, for cover crop 1", required=True
    )
    # 24c
    cover_crop_planting_rate_1_units = forms.ChoiceField(
        label="Units for cover crop 1",
        choices=CoverCropRateUnitsChoices.choices,
        required=True,
    )
    # Species 2
    # 25a
    cover_crop_species_2 = forms.ChoiceField(
        label="25. Cover crop 2",
        choices=CoverCropChoices.choices,
        required=False,
    )
    # 25b
    cover_crop_planting_rate_2 = forms.IntegerField(
        label="Planting rate, for cover crop 2", required=False
    )
    # 25c
    cover_crop_planting_rate_2_units = forms.ChoiceField(
        label="Units for cover crop 2",
        choices=CoverCropRateUnitsChoices.choices,
        required=False,
    )
    # Species 3
    # 26
    cover_crop_species_3 = forms.ChoiceField(
        label="26. Cover crop 3",
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
    # 27
    cover_crop_species_4 = forms.ChoiceField(
        label="27. Cover crop 4",
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
    # 28
    cover_crop_species_5 = forms.ChoiceField(
        label="28. Cover crop 5",
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

    # 29
    cover_crop_species_and_rate_write_in = forms.CharField(
        label="29. Other cover crops planted and their rates, please specify in pounds per acre.",
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=500,
        required=False,
    )
    # 30
    cover_crop_multispecies_mix_write_in = forms.CharField(
        label="30. If you planted a multispecies mix in 2023 please provide details.",
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=500,
        required=False,
    )

    # 31	What date this year did you plant your cash crop in this field?
    cash_crop_planting_date = forms.DateField(
        label="31. What date this year did you plant your cash crop in this field? (Estimate is OK if not known)",
        required=True,
    )
    # 32	How many years have you been planting cover crops *in this field*?
    years_with_cover_crops = forms.IntegerField(
        label="32. How many years have you been planting cover crops *in this field*?",
        required=True,
        min_value=0,
        max_value=100,
    )
    # 33	"Please choose the dominant soil texture of the field.
    dominant_soil_texture = forms.ChoiceField(
        label="33. Please select the dominant soil texture of this field.",
        choices=SoilTextureClassChoices.choices,
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
            "cover_crop_species_and_rate_write_in",
            "cover_crop_multispecies_mix_write_in",
            "cash_crop_planting_date",
            "years_with_cover_crops",
            "dominant_soil_texture",
        )


class SurveyFieldFormFull_2023_partb(forms.ModelForm):

    # 37a	Will you apply manure prior to seeding cover crops on this field, and at what rate?
    manure_prior = forms.ChoiceField(
        label="37. Will you apply manure prior to seeding cover crops on this field?",
        required=True,
        choices=TRUE_FALSE_CHOICES,
    )
    # 37b
    manure_prior_rate = forms.IntegerField(
        label="At what rate will the manure be applied?",
        required=False,
        min_value=0,
    )
    # 37c
    manure_prior_rate_units = forms.ChoiceField(
        label="Please select the units for the manure application rate.",
        choices=ManureApplicateUnitsChoices.choices,
        required=False,
    )

    # 38a Will manure be applied to the field after the cover crop is established?
    manure_post = forms.ChoiceField(
        label="38. Will manure be applied to the field after the cover crop is established?",
        required=True,
        choices=TRUE_FALSE_CHOICES,
    )
    # 38b
    manure_post_rate = forms.IntegerField(
        label="At what rate will the manure be applied?",
        required=False,
        min_value=0,
    )
    # 38c
    manure_post_rate_units = forms.ChoiceField(
        label="The units for the manure application rate",
        choices=ManureApplicateUnitsChoices.choices,
        required=False,
    )
    # 39	"What is your tillage system for the cash crop preceding the cover crop?
    tillage_system_cash_crop = forms.ChoiceField(
        label="39. What is your tillage system for the cash crop preceding the cover crop?",
        choices=TillageSystemChoices.choices,
        required=True,
    )
    # 40a	"Primary tillage equipment (select all that apply) for a cash crop preceding a cover crop?
    primary_tillage_equipment = forms.ChoiceField(
        label="40. Primary tillage equipment (select all that apply) for a cash crop preceding a cover crop?",
        choices=PrimaryTillageEquipmentChoices.choices,
        required=True,
    )
    # 40b
    primary_tillage_equipment_write_in = forms.CharField(
        label="If you selected other, please explain.",
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=500,
        required=False,
    )
    # 41	"Secondary tillage equipment (select all that apply) for cash crop preceding the cover crop?
    secondary_tillage_equipment = forms.ChoiceField(
        label="41. Secondary tillage equipment (select all that apply) for cash crop preceding the cover crop?",
        choices=SecondaryTillageEquipmentChoices.choices,
        required=False,
    )
    secondary_tillage_equipment_write_in = forms.CharField(
        label="If you selected other, please explain.",
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=500,
        required=False,
    )

    # 42	"Soil conditions in this field at cover crop seeding
    soil_conditions_at_cover_crop_seeding = forms.ChoiceField(
        label="42. Soil conditions in this field at cover crop seeding.",
        choices=SoilConditionsSeedingChoices.choices,
        required=True,
    )

    # 43	"Cover Crop Seeding Method.
    cover_crop_seeding_method = forms.ChoiceField(
        label="43. Please select your the seeding method for your cover crop.",
        choices=SeedingMethodChoices.choices,
        required=True,
    )

    # 43 b
    cover_crop_seeding_method_write_in = forms.CharField(
        label="If you selected other, please explain.",
        widget=forms.Textarea(attrs={"rows": 5}),
        max_length=500,
        required=False,
    )

    # 44
    cover_crop_seed_cost = forms.IntegerField(
        label="44. Estimated cover crop seed cost for this field ($/acre)",
        min_value=0,
        required=True,
    )
    # 45	Estimated cover crop planting cost per acre in this field. Please use UW Extension Custom Rate Guide.(https://www.nass.usda.gov/Statistics_by_State/Wisconsin/Publications/WI-CRate20.pdf)
    cover_crop_planting_cost = forms.IntegerField(
        label='45. Estimated cover crop planting cost per acre in this field. Please use <a href="https://www.nass.usda.gov/Statistics_by_State/Wisconsin/Publications/WI-CRate20.pdf" target="_blank" rel="noopener noreferrer">UW Extension Custom Rate Guide.</a>',
        min_value=0,
        required=True,
    )
    # 46	Cover crop planting date for this field (estimate is OK if not known).
    cover_crop_planting_date = forms.DateField(
        label="46. Cover crop planting date for this field (estimate is OK if not known).",
        required=True,
    )
    # 47	"Estimated termination timing/method for this field.
    cover_crop_estimated_termination = forms.ChoiceField(
        label="47. Estimated termination timing/method for this field.",
        choices=TerminationMethodTimingChoices.choices,
        required=True,
    )

    # 48	Number of days estimated between crop harvest and cover crop establishment in this field.
    days_between_crop_hvst_and_cc_estd = forms.IntegerField(
        label="48. Number of days estimated between crop harvest and cover crop establishment in this field.",
        min_value=0,
        max_value=365,
        required=True,
    )

    class Meta:
        model = SurveyField
        fields = (
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
            "cover_crop_planting_date",
            "cover_crop_estimated_termination",
            "days_between_crop_hvst_and_cc_estd",
        )
