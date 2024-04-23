from wisccc.models import Survey, Farmer
from django.contrib.auth import get_user_model

import pandas as pd


def ingest_2022_data():
    """CitSci CCROP 2022 responses agronomic.xlsx"""
    pass


# Get the unassigned user or create if not exists
unassigned_user = get_user_model().objects.filter(username="Unassigned").first()

if unassigned_user is None:
    unassigned_user = get_user_model().objects.create_user(
        username="Unassigned", email="horrorshowdream@hotmail.com", password="shitfire"
    )

unassigned_farmer = Farmer.objects.filter(first_name="Unassigned Firstname").first()

if unassigned_farmer is None:
    unassigned_farmer = Farmer.objects.create(
        first_name="Unassigned Firstname",
        last_name="Unassigned Lastname",
        farm_name="Unassigned Farm",
        county="Unassigned county",
        user=unassigned_user,
    )


fl_full_data = "~/Documents/small_projects/wisc_cc/data_from_mrill/2022 Responses - Building Knowledge about Wisconsin's Cover Crops.xlsx"
fl_data = "~/Documents/small_projects/wisc_cc/data_from_mrill/CitSci CCROP 2022 responses agronomic.xlsx"

dat = pd.read_excel(fl_data, header=0)
cols = dat.columns

full_data = pd.read_excel(fl_full_data)
for i, col in enumerate(full_data.columns):
    print(f"{i}: {col}")


def get_ranked_choices(row_position, start_col, end_col):
    """End col should be the position of the last col plus 1
    2. nutrient mngmt: 3,9
    6. cov crop info: 14, 24
    8. cov crop motivation: 26, 39
    9. influence cov: 40, 50
    """
    indx_list = [indx for indx in range(start_col, end_col)]

    tmp_df = pd.DataFrame(
        {
            "options": cols_full_data[start_col:end_col],
            "choices": full_data.iloc[row_position, indx_list],
            "ranked": full_data.iloc[row_position, indx_list],
        }
    )
    tmp_df.ranked.where(tmp_df.choices != "Most important", 1, inplace=True)
    tmp_df.ranked.where(tmp_df.choices != "More important", 2, inplace=True)
    tmp_df.ranked.where(tmp_df.choices != "Important", 3, inplace=True)
    tmp_df.ranked.where(tmp_df.choices != "Somewhat important", 4, inplace=True)
    tmp_df.ranked.where(tmp_df.choices != "Least important", 5, inplace=True)

    ranked_options = tmp_df.sort_values(by="ranked").options.tolist()

    return ranked_options


cols_full_data = full_data.columns
cols_full_data = [
    col.replace(
        "2. Where do you go for nutrient management recommendations? Select and rank all that apply. [",
        "",
    ).replace("]", "")
    for col in cols_full_data
]
cols_full_data = [
    col.replace(
        "6. Where do you go for cover cropping information? Select and rank all that apply.  [",
        "",
    ).replace("]", "")
    for col in cols_full_data
]
cols_full_data = [
    col.replace(
        "8. What motivates you to cover crop? Please select and rank all that apply. [",
        "",
    ).replace("]", "")
    for col in cols_full_data
]
cols_full_data = [
    col.replace(
        "9. Do, or might, any of the following positively influence your decision to cover crop? Please select and rank all that apply. [",
        "",
    ).replace("]", "")
    for col in cols_full_data
]


# for i in range(len(dat)):
i = 0
# ------------------------------------------------ #
# Where do you go for nutrient management recommendations? Select and rank all that apply.
info_source_nutrient_mgmt = get_ranked_choices(i, 3, 9)
# 6. Where do you go for cover cropping information? Select and rank all that apply.
info_source_cover_crops = get_ranked_choices(i, 14, 24)
# 8. What motivates you to cover crop? Please select and rank all that apply.
motivation = get_ranked_choices(i, 26, 39)
# 9. Do, or might, any of the following positively influence your decision to cover crop? Please select and rank all that apply.
cov_crop_influence = get_ranked_choices(i, 40, 50)
# ------------------------------------------------ #
# Dominant soil series
dom_soil_series = full_data.iloc[i][25].split(",")
dom_soil_series_1 = dom_soil_series[0]
dom_soil_series_2 = None
dom_soil_series_3 = None
dom_soil_series_4 = None
if len(dom_soil_series) > 1:
    dom_soil_series_2 = dom_soil_series[1]
if len(dom_soil_series) > 2:
    dom_soil_series_3 = dom_soil_series[2]
if len(dom_soil_series) > 3:
    dom_soil_series_4 = dom_soil_series[4:]
# ------------------------------------------------ #
# Cover crop species
cover_crop_species = full_data.iloc[i][61].split(", ")
cover_crop_species_1 = cover_crop_species[0]
cover_crop_species_2 = None
cover_crop_species_3 = None
cover_crop_species_4 = None
cover_crop_species_5 = None
if len(cover_crop_species) > 1:
    cover_crop_species_2 = cover_crop_species[1]

if len(cover_crop_species) > 2:
    cover_crop_species_3 = cover_crop_species[2]

if len(cover_crop_species) > 3:
    cover_crop_species_4 = cover_crop_species[3]

if len(cover_crop_species) > 4:
    cover_crop_species_5 = cover_crop_species[4]

if len(cover_crop_species) > 5:
    cover_crop_species_and_rate_write_in = cover_crop_species[5:]

# ------------------------------------------------ #
# Cover crop planting rates
cover_crop_planting_rates = full_data.iloc[i][75].split(",")
cover_crop_planting_rate_2 = None
cover_crop_planting_rate_3 = None
cover_crop_planting_rate_4 = None
cover_crop_planting_rate_5 = None
cover_crop_planting_rate_1 = cover_crop_planting_rates[0]
if len(cover_crop_planting_rates) > 1:
    cover_crop_planting_rate_2 = cover_crop_planting_rates[1]
if len(cover_crop_planting_rates) > 2:
    cover_crop_planting_rate_3 = cover_crop_planting_rates[2]
if len(cover_crop_planting_rates) > 3:
    cover_crop_planting_rate_4 = cover_crop_planting_rates[3]
if len(cover_crop_planting_rates) > 4:
    cover_crop_planting_rate_5 = cover_crop_planting_rates[4]

# ------------------------------------------------ #
new_survey = Survey.objects.create(
    survey_year=2022,
    years_experience=full_data.iloc[i][11],
    total_acres=full_data.iloc[i][12],
    percent_of_farm_cc=full_data.iloc[i][13],
    dominant_soil_series_1=dom_soil_series_1,
    dominant_soil_series_2=dom_soil_series_2,
    dominant_soil_series_3=dom_soil_series_3,
    dominant_soil_series_4=dom_soil_series_4,
    info_source_nutrient_mgmt_1=info_source_nutrient_mgmt[0],
    info_source_nutrient_mgmt_2=info_source_nutrient_mgmt[1],
    info_source_nutrient_mgmt_3=info_source_nutrient_mgmt[2],
    source_nutrient_mgmt_write_in=info_source_nutrient_mgmt[3:]
    + [", ", full_data.iloc[i][9]],
    cov_crops_for_ntrnt_mgmt_comments_questions=full_data.iloc[i][10],
    info_source_cover_crops_1=info_source_cover_crops[0],
    info_source_cover_crops_2=info_source_cover_crops[1],
    info_source_cover_crops_3=info_source_cover_crops[2],
    info_source_cover_crops_write_in=info_source_cover_crops[3:]
    + ["\n", full_data.iloc[i][24]],
    support_cover_crops_1=None,
    support_cover_crops_2=None,
    support_cover_crops_3=None,
    support_cover_crops_write_in=None,
    lacking_any_info_cover_crops=full_data.iloc[i][50],
    barriers_to_expansion=full_data.iloc[i][52],
    quit_planting_cover_crops=full_data.iloc[i][53],
    if_use_crop_insurance=full_data.iloc[i][54],
    why_cover_crops_write_in=motivation + ["\n", full_data.iloc[i][39]],
    cover_crops_delay_cash_crop=full_data.iloc[i][55],
    save_cover_crop_seed=None,
    source_cover_crop_seed=None,
    closest_zip_code=full_data.iloc[i][56],
    field_acreage=full_data.iloc[i][59],
    crop_rotation=full_data.iloc[i][60],
    crop_rotation_2021_cover_crop_species=None,
    crop_rotation_2021_cash_crop_species=None,
    crop_rotation_2022_cover_crop_species=None,
    crop_rotation_2022_cash_crop_species=None,
    crop_rotation_2023_cover_crop_species=None,
    crop_rotation_2023_cash_crop_species=None,
    cover_crop_species_1=cover_crop_species_1,
    cover_crop_planting_rate_1=cover_crop_planting_rate_1,
    cover_crop_species_2=cover_crop_species_2,
    cover_crop_planting_rate_2=cover_crop_planting_rate_2,
    cover_crop_species_3=cover_crop_species_3,
    cover_crop_planting_rate_3=cover_crop_planting_rate_3,
    cover_crop_species_4=cover_crop_species_4,
    cover_crop_planting_rate_4=cover_crop_planting_rate_4,
    cover_crop_species_5=cover_crop_species_5,
    cover_crop_planting_rate_5=cover_crop_planting_rate_5,
    cover_crop_species_and_rate_write_in=cover_crop_species_and_rate_write_in,
    cash_crop_planting_date=full_data.iloc[i][63],
    years_with_cover_crops=full_data.iloc[i][64],
    dominant_soil_texture=full_data.iloc[i][65],
    manure_prior=full_data.iloc[i][66],
    manure_prior_rate=full_data.iloc[i][69],
    manure_prior_rate_units=(
        full_data.iloc[i][68] if not pd.isna(full_data.iloc[i][68]) else None
    ),
    manure_post=full_data.iloc[i][67],
    manure_post_rate=full_data.iloc[i][69],
    manure_post_rate_units=full_data.iloc[i][68],
    tillage_system_cash_crop=full_data.iloc[i][70],
    primary_tillage_equipment=full_data.iloc[i][71],
    primary_tillage_equipment_write_in=None,
    secondary_tillage_equipment=full_data.iloc[i][72],
    secondary_tillage_equipment_write_in=None,
    soil_conditions_at_cover_crop_seeding=full_data.iloc[i][73],
    cover_crop_seeding_method=full_data.iloc[i][74],
    cover_crop_seeding_method_write_in=None,
    cover_crop_seed_cost=full_data.iloc[i][76],
    cover_crop_planting_cost=(
        full_data.iloc[i][77] if not pd.isna(full_data.iloc[i][77]) else None
    ),
    cover_crop_planting_date=full_data.iloc[i][78],
    cover_crop_estimated_termination=full_data.iloc[i][79],
    days_between_crop_hvst_and_cc_estd=full_data.iloc[i][80],
    interesting_tales=full_data.iloc[i][81],
    where_to_start=None,
    additional_thoughts=full_data.iloc[i][82],
    user=unassigned_user,
    farm_location=None,
    last_updated=None,
    survey_created=None,
    confirmed_accurate=True,
    cover_crop_multispecies_mix_write_in=None,
    cover_crop_planting_rate_1_units=full_data.iloc[i][75],
    cover_crop_planting_rate_2_units=None,
    cover_crop_planting_rate_3_units=None,
    cover_crop_planting_rate_4_units=None,
    cover_crop_planting_rate_5_units=None,
    notes_admin=None,
)


# derived_county
# derived_species_class


new_survey = Survey.objects.create()

new_survey.survey_year
new_survey.years_experience
new_survey.total_acres
new_survey.percent_of_farm_cc
new_survey.dominant_soil_series_1
new_survey.dominant_soil_series_2
new_survey.dominant_soil_series_3
new_survey.dominant_soil_series_4
new_survey.info_source_nutrient_mgmt_1
new_survey.info_source_nutrient_mgmt_2
new_survey.info_source_nutrient_mgmt_3
new_survey.source_nutrient_mgmt_write_in
new_survey.cov_crops_for_ntrnt_mgmt_comments_questions
new_survey.info_source_cover_crops_1
new_survey.info_source_cover_crops_2
new_survey.info_source_cover_crops_3
new_survey.info_source_cover_crops_write_in
new_survey.support_cover_crops_1
new_survey.support_cover_crops_2
new_survey.support_cover_crops_3
new_survey.support_cover_crops_write_in
new_survey.lacking_any_info_cover_crops
new_survey.barriers_to_expansion
new_survey.quit_planting_cover_crops
new_survey.if_use_crop_insurance
new_survey.why_cover_crops_write_in
new_survey.cover_crops_delay_cash_crop
new_survey.save_cover_crop_seed
new_survey.source_cover_crop_seed
new_survey.closest_zip_code
new_survey.field_acreage
new_survey.crop_rotation
new_survey.crop_rotation_2021_cover_crop_species
new_survey.crop_rotation_2021_cash_crop_species
new_survey.crop_rotation_2022_cover_crop_species
new_survey.crop_rotation_2022_cash_crop_species
new_survey.crop_rotation_2023_cover_crop_species
new_survey.crop_rotation_2023_cash_crop_species
new_survey.cover_crop_species_1
new_survey.cover_crop_planting_rate_1
new_survey.cover_crop_species_2
new_survey.cover_crop_planting_rate_2
new_survey.cover_crop_species_3
new_survey.cover_crop_planting_rate_3
new_survey.cover_crop_species_4
new_survey.cover_crop_planting_rate_4
new_survey.cover_crop_species_5
new_survey.cover_crop_planting_rate_5
new_survey.cover_crop_species_and_rate_write_in
new_survey.cash_crop_planting_date
new_survey.years_with_cover_crops
new_survey.dominant_soil_texture
new_survey.manure_prior
new_survey.manure_prior_rate
new_survey.manure_prior_rate_units
new_survey.manure_post
new_survey.manure_post_rate
new_survey.manure_post_rate_units
new_survey.tillage_system_cash_crop
new_survey.primary_tillage_equipment
new_survey.primary_tillage_equipment_write_in
new_survey.secondary_tillage_equipment
new_survey.secondary_tillage_equipment_write_in
new_survey.soil_conditions_at_cover_crop_seeding
new_survey.cover_crop_seeding_method
new_survey.cover_crop_seeding_method_write_in
new_survey.cover_crop_seed_cost
new_survey.cover_crop_planting_cost
new_survey.cover_crop_planting_date
new_survey.cover_crop_estimated_termination
new_survey.days_between_crop_hvst_and_cc_estd
new_survey.interesting_tales
new_survey.where_to_start
new_survey.additional_thoughts
new_survey.user
new_survey.farm_location
new_survey.last_updated
new_survey.survey_created
new_survey.confirmed_accurate
new_survey.cover_crop_multispecies_mix_write_in
new_survey.cover_crop_planting_rate_1_units
new_survey.cover_crop_planting_rate_2_units
new_survey.cover_crop_planting_rate_3_units
new_survey.cover_crop_planting_rate_4_units
new_survey.cover_crop_planting_rate_5_units
new_survey.notes_admin
# new_survey.derived_county
# new_survey.derived_species_class
