from wisccc.models import Survey, Farmer
from django.contrib.auth import get_user_model

import pandas as pd


def ingest_2022_data():
    """CitSci CCROP 2022 responses agronomic.xlsx"""

    # Get the unassigned user or create if not exists
    unassigned_user = get_user_model().objects.filter(username="Unassigned").first()

    if unassigned_user is None:
        unassigned_user = get_user_model().objects.create_user(
            username="Unassigned",
            email="horrorshowdream@hotmail.com",
            password="shitfire",
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
        'Less motivating', 'Primary motivation', 'Somewhat motivating'
        9. influence cov: 40, 50
        "Not really influential", "Maybe influential", "Very influential"


        """
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
        indx_list = [indx for indx in range(start_col, end_col)]

        tmp_df = pd.DataFrame(
            {
                "options": cols_full_data[start_col:end_col],
                "choices": full_data.iloc[row_position, indx_list],
                "ranked": full_data.iloc[row_position, indx_list],
            }
        )
        if start_col == 26:
            tmp_df.ranked.where(tmp_df.choices != "Primary motivation", 1, inplace=True)
            tmp_df.ranked.where(
                tmp_df.choices != "Somewhat motivating", 2, inplace=True
            )
            tmp_df.ranked.where(tmp_df.choices != "Less motivating", 3, inplace=True)
        elif start_col == 40:
            tmp_df.ranked.where(tmp_df.choices != "Very influential", 1, inplace=True)
            tmp_df.ranked.where(tmp_df.choices != "Maybe influential", 2, inplace=True)
            tmp_df.ranked.where(
                tmp_df.choices != "Not really influential", 3, inplace=True
            )
        else:
            tmp_df.ranked.where(tmp_df.choices != "Most important", 1, inplace=True)
            tmp_df.ranked.where(tmp_df.choices != "More important", 2, inplace=True)
            tmp_df.ranked.where(tmp_df.choices != "Important", 3, inplace=True)
            tmp_df.ranked.where(tmp_df.choices != "Somewhat important", 4, inplace=True)
            tmp_df.ranked.where(tmp_df.choices != "Least important", 5, inplace=True)

        ranked_options = tmp_df.sort_values(by="ranked").options.tolist()

        return ranked_options

    for i in range(len(full_data)):
        # i = 0
        # ------------------------------------------------ #
        # Where do you go for nutrient management recommendations? Select and rank all that apply.
        info_source_nutrient_mgmt = get_ranked_choices(i, 3, 9)
        info_source_nutrient_mgmt_2 = None
        info_source_nutrient_mgmt_3 = None
        source_nutrient_mgmt_write_in = None
        info_source_nutrient_mgmt_we_missed = (
            full_data.iloc[i][9] if not pd.isna(full_data.iloc[i][9]) else None
        )
        info_source_nutrient_mgmt_1 = info_source_nutrient_mgmt[0]
        if len(info_source_nutrient_mgmt) > 1:
            info_source_nutrient_mgmt_2 = info_source_nutrient_mgmt[1]
        if len(info_source_nutrient_mgmt) > 2:
            info_source_nutrient_mgmt_3 = info_source_nutrient_mgmt[2]
        if len(info_source_nutrient_mgmt) > 3:
            source_nutrient_mgmt_write_in = ",".join(info_source_nutrient_mgmt[3:])
        if info_source_nutrient_mgmt_we_missed:
            source_nutrient_mgmt_write_in += info_source_nutrient_mgmt_we_missed

        # 6. Where do you go for cover cropping information? Select and rank all that apply.
        info_source_cover_crops = get_ranked_choices(i, 14, 24)
        info_source_cover_crops_2 = None
        info_source_cover_crops_3 = None
        info_source_cover_crops_write_in = None
        info_source_cover_crops_1 = info_source_cover_crops[0]
        info_source_cover_crops_missed = (
            full_data.iloc[i][24] if not pd.isna(full_data.iloc[i][24]) else None
        )
        if len(info_source_cover_crops) > 1:
            info_source_cover_crops_2 = info_source_cover_crops[1]
        if len(info_source_cover_crops) > 2:
            info_source_cover_crops_3 = info_source_cover_crops[2]
        if len(info_source_cover_crops) > 3:
            info_source_cover_crops_write_in = ",".join(info_source_cover_crops[3:])
        if info_source_cover_crops_missed:
            info_source_cover_crops_write_in += info_source_cover_crops_missed
        # 8. What motivates you to cover crop? Please select and rank all that apply.
        motivation = ",".join(get_ranked_choices(i, 26, 39))
        missed_motivations = full_data.iloc[i][39]
        if not pd.isna(full_data.iloc[i][39]) and missed_motivations.lower() != "no":
            motivation + "," + missed_motivations

        # 9. Do, or might, any of the following positively influence your decision to cover crop? Please select and rank all that apply.
        cov_crop_influence = get_ranked_choices(i, 40, 50)
        support_cover_crops_1 = cov_crop_influence[0]
        support_cover_crops_2 = None
        support_cover_crops_3 = None
        support_cover_crops_write_in = None
        if len(cov_crop_influence) > 1:
            support_cover_crops_2 = cov_crop_influence[1]
        if len(cov_crop_influence) > 2:
            support_cover_crops_3 = cov_crop_influence[2]
        if len(cov_crop_influence) > 3:
            support_cover_crops_write_in = ",".join(cov_crop_influence[3:])
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
        cover_crop_species_and_rate_write_in = None
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

        cover_crop_planting_rates = (
            full_data.iloc[i][75] if not pd.isna(full_data.iloc[i][75]) else None
        )

        try:
            cover_crop_planting_rates = cover_crop_planting_rates.split(",")
        except:
            cover_crop_planting_rates = [cover_crop_planting_rates]
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
            info_source_nutrient_mgmt_1=info_source_nutrient_mgmt_1,
            info_source_nutrient_mgmt_2=info_source_nutrient_mgmt_2,
            info_source_nutrient_mgmt_3=info_source_nutrient_mgmt_3,
            source_nutrient_mgmt_write_in=source_nutrient_mgmt_write_in,
            cov_crops_for_ntrnt_mgmt_comments_questions=(
                full_data.iloc[i][10] if not pd.isna(full_data.iloc[i][10]) else None
            ),
            info_source_cover_crops_1=info_source_cover_crops_1,
            info_source_cover_crops_2=info_source_cover_crops_2,
            info_source_cover_crops_3=info_source_cover_crops_3,
            info_source_cover_crops_write_in=info_source_cover_crops_write_in,
            support_cover_crops_1=support_cover_crops_1,
            support_cover_crops_2=support_cover_crops_2,
            support_cover_crops_3=support_cover_crops_3,
            support_cover_crops_write_in=support_cover_crops_write_in,
            lacking_any_info_cover_crops=full_data.iloc[i][50],
            barriers_to_expansion=(
                full_data.iloc[i][52] if not pd.isna(full_data.iloc[i][52]) else None
            ),
            quit_planting_cover_crops=(
                full_data.iloc[i][53] if not pd.isna(full_data.iloc[i][53]) else None
            ),
            if_use_crop_insurance=full_data.iloc[i][54],
            why_cover_crops_write_in=motivation,
            cover_crops_delay_cash_crop=(
                full_data.iloc[i][55] if not pd.isna(full_data.iloc[i][55]) else None
            ),
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
            years_with_cover_crops=(
                full_data.iloc[i][64] if not pd.isna(full_data.iloc[i][64]) else None
            ),
            dominant_soil_texture=full_data.iloc[i][65],
            manure_prior=full_data.iloc[i][66],
            manure_prior_rate=(
                full_data.iloc[i][69] if not pd.isna(full_data.iloc[i][69]) else None
            ),
            manure_prior_rate_units=(
                full_data.iloc[i][68] if not pd.isna(full_data.iloc[i][68]) else None
            ),
            manure_post=full_data.iloc[i][67],
            manure_post_rate=(
                full_data.iloc[i][69] if not pd.isna(full_data.iloc[i][69]) else None
            ),
            manure_post_rate_units=full_data.iloc[i][68],
            tillage_system_cash_crop=full_data.iloc[i][70],
            primary_tillage_equipment=(
                full_data.iloc[i][71] if not pd.isna(full_data.iloc[i][71]) else None
            ),
            primary_tillage_equipment_write_in=None,
            secondary_tillage_equipment=(
                full_data.iloc[i][72] if not pd.isna(full_data.iloc[i][72]) else None
            ),
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
            cover_crop_planting_rate_1_units="lbs/acre",
            cover_crop_planting_rate_2_units=None,
            cover_crop_planting_rate_3_units=None,
            cover_crop_planting_rate_4_units=None,
            cover_crop_planting_rate_5_units=None,
            notes_admin=None,
        )


def ingest_2020_1_data():

    # Get the unassigned user or create if not exists
    unassigned_user = get_user_model().objects.filter(username="Unassigned").first()

    if unassigned_user is None:
        unassigned_user = get_user_model().objects.create_user(
            username="Unassigned",
            email="horrorshowdream@hotmail.com",
            password="shitfire",
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

    fl_full_data = "~/Documents/small_projects/wisc_cc/data_from_mrill/MI Copy combined CC_citsci_2020-2021-grs.xlsx"

    full_data = pd.read_excel(fl_full_data)
    for i, col in enumerate(full_data.columns):
        print(f"{i}: {col}")

    for i in range(len(full_data)):
        # i = 0
        # info source nutrient management
        info_source_nutrient_mgmt = full_data.iloc[i][57].split(", ")
        info_source_nutrient_mgmt_1 = None
        info_source_nutrient_mgmt_2 = None
        info_source_nutrient_mgmt_3 = None
        source_nutrient_mgmt_write_in = None
        if info_source_nutrient_mgmt != ["."]:
            info_source_nutrient_mgmt_1 = info_source_nutrient_mgmt[0]
            if len(info_source_nutrient_mgmt) > 1:
                info_source_nutrient_mgmt_2 = info_source_nutrient_mgmt[1]
            if len(info_source_nutrient_mgmt) > 2:
                info_source_nutrient_mgmt_3 = info_source_nutrient_mgmt[2]
            if len(info_source_nutrient_mgmt) > 3:
                source_nutrient_mgmt_write_in = ",".join(info_source_nutrient_mgmt[3:])

        # source_cc_info to info_source_cover_crops
        info_source_cover_crops = full_data.iloc[i][60].split(", ")
        info_source_cover_crops_1 = None
        info_source_cover_crops_2 = None
        info_source_cover_crops_3 = None
        info_source_cover_crops_write_in = None
        if info_source_cover_crops != ["."]:
            info_source_cover_crops_1 = info_source_cover_crops[0]
            if len(info_source_cover_crops) > 1:
                info_source_cover_crops_2 = info_source_cover_crops[1]
            if len(info_source_cover_crops) > 2:
                info_source_cover_crops_3 = info_source_cover_crops[2]
            if len(info_source_cover_crops) > 3:
                source_cover_crops_write_in = ",".join(info_source_cover_crops[3:])

        # Influence being slotted into support
        support_cover_crops = full_data.iloc[i][62].split(", ")
        support_cover_crops_1 = None
        support_cover_crops_2 = None
        support_cover_crops_3 = None
        support_cover_crops_write_in = None

        if support_cover_crops != ["."]:
            support_cover_crops_1 = support_cover_crops[0]
            if len(support_cover_crops) > 1:
                support_cover_crops_2 = support_cover_crops[1]
            if len(support_cover_crops) > 2:
                support_cover_crops_3 = support_cover_crops[2]
            if len(support_cover_crops) > 3:
                support_cover_crops_write_in = ",".join(support_cover_crops[3:])

        # Cover crop splitting
        cover_crop_species = full_data.iloc[i][15]
        # removing this text which was present in 2020
        cover_crop_species = cover_crop_species.replace(
            "multispecies mix (please list below): ", ""
        )
        cover_crop_species = cover_crop_species.split(",")
        cover_crop_species_1 = None
        cover_crop_species_2 = None
        cover_crop_species_3 = None
        cover_crop_species_4 = None
        cover_crop_species_5 = None
        cover_crop_species_and_rate_write_in = None
        if cover_crop_species != ["."]:
            cover_crop_species_1 = cover_crop_species[0]
            if len(cover_crop_species) > 1:
                cover_crop_species_2 = cover_crop_species[1]
            if len(cover_crop_species) > 2:
                cover_crop_species_3 = cover_crop_species[2]
            if len(cover_crop_species) > 3:
                cover_crop_species_4 = cover_crop_species[3]
            if len(cover_crop_species) > 4:
                cover_crop_species_5 = cover_crop_species[4]
            if len(cover_crop_species) > 5:
                cover_crop_species_and_rate_write_in = ",".join(cover_crop_species[6:])

        new_survey = Survey.objects.create(
            survey_year=full_data.iloc[i][0],
            years_experience=full_data.iloc[i][13],
            total_acres=(
                full_data.iloc[i][17] if not full_data.iloc[i][17] == "." else None
            ),
            percent_of_farm_cc=(
                full_data.iloc[i][16] if not full_data.iloc[i][16] == "." else None
            ),
            dominant_soil_series_1=full_data.iloc[i][55],
            dominant_soil_series_2=None,
            dominant_soil_series_3=None,
            dominant_soil_series_4=None,
            info_source_nutrient_mgmt_1=info_source_nutrient_mgmt_1,
            info_source_nutrient_mgmt_2=info_source_nutrient_mgmt_2,
            info_source_nutrient_mgmt_3=info_source_nutrient_mgmt_3,
            source_nutrient_mgmt_write_in=source_nutrient_mgmt_write_in,
            cov_crops_for_ntrnt_mgmt_comments_questions=full_data.iloc[i][59],
            info_source_cover_crops_1=info_source_cover_crops_1,
            info_source_cover_crops_2=info_source_cover_crops_2,
            info_source_cover_crops_3=info_source_cover_crops_3,
            info_source_cover_crops_write_in=source_cover_crops_write_in,
            support_cover_crops_1=support_cover_crops_1,
            support_cover_crops_2=support_cover_crops_2,
            support_cover_crops_3=support_cover_crops_3,
            support_cover_crops_write_in=support_cover_crops_write_in,
            lacking_any_info_cover_crops=full_data.iloc[i][66],
            barriers_to_expansion=full_data.iloc[i][64] + " - " + full_data.iloc[i][65],
            quit_planting_cover_crops=None,
            if_use_crop_insurance=None,
            why_cover_crops_write_in=None,
            cover_crops_delay_cash_crop=None,
            save_cover_crop_seed=None,
            source_cover_crop_seed=None,
            closest_zip_code=full_data.iloc[i][4],
            field_acreage=(
                full_data.iloc[i][18] if not full_data.iloc[i][18] == "." else None
            ),
            crop_rotation="Not asked this year.",
            crop_rotation_2021_cover_crop_species=None,
            crop_rotation_2021_cash_crop_species=None,
            crop_rotation_2022_cover_crop_species=None,
            crop_rotation_2022_cash_crop_species=None,
            crop_rotation_2023_cover_crop_species=None,
            crop_rotation_2023_cash_crop_species=None,
            cover_crop_species_1=cover_crop_species_1,
            cover_crop_species_2=cover_crop_species_2,
            cover_crop_species_3=cover_crop_species_3,
            cover_crop_species_4=cover_crop_species_4,
            cover_crop_species_5=cover_crop_species_5,
            cover_crop_multispecies_mix_write_in=cover_crop_species_and_rate_write_in,
            cover_crop_planting_rate_1=full_data.iloc[i][66],
            cover_crop_planting_rate_2=None,
            cover_crop_planting_rate_3=None,
            cover_crop_planting_rate_4=None,
            cover_crop_planting_rate_5=None,
            cover_crop_species_and_rate_write_in=None,
            cash_crop_planting_date=None,
            years_with_cover_crops=(
                full_data.iloc[i][12] if not full_data.iloc[i][12] == "." else None
            ),
            dominant_soil_texture=full_data.iloc[i][56],
            manure_prior=full_data.iloc[i][8],
            manure_prior_rate=full_data.iloc[i][10],
            manure_prior_rate_units=full_data.iloc[i][11],
            manure_post=full_data.iloc[i][9],
            manure_post_rate=full_data.iloc[i][10],
            manure_post_rate_units=full_data.iloc[i][11],
            tillage_system_cash_crop=full_data.iloc[i][47],
            primary_tillage_equipment=full_data.iloc[i][48],
            primary_tillage_equipment_write_in=None,
            secondary_tillage_equipment=full_data.iloc[i][49],
            secondary_tillage_equipment_write_in=None,
            soil_conditions_at_cover_crop_seeding=full_data.iloc[i][22],
            cover_crop_seeding_method=full_data.iloc[i][21],
            cover_crop_seeding_method_write_in=None,
            cover_crop_seed_cost=(
                full_data.iloc[i][23] if not full_data.iloc[i][23] == "." else None
            ),
            cover_crop_planting_cost=(
                full_data.iloc[i][24] if not full_data.iloc[i][24] == "." else None
            ),
            cover_crop_planting_date=full_data.iloc[i][25],
            cover_crop_estimated_termination=full_data.iloc[i][28],
            days_between_crop_hvst_and_cc_estd=None,
            interesting_tales=None,
            where_to_start=None,
            additional_thoughts=(
                full_data.iloc[i][68] if not pd.isna(full_data.iloc[i][68]) else None
            ),
            user=unassigned_user,
            farm_location=None,
            confirmed_accurate=False,
            cover_crop_planting_rate_1_units="lbs/acre",
            cover_crop_planting_rate_2_units="lbs/acre",
            cover_crop_planting_rate_3_units="lbs/acre",
            cover_crop_planting_rate_4_units="lbs/acre",
            cover_crop_planting_rate_5_units="lbs/acre",
            notes_admin="Added automatically. Note manure rates and units are assigned to both pre and post values because it was unspecified during these survey years.",
        )
