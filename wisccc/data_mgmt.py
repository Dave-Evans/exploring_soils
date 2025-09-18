import json
import pandas as pd
from django.http import HttpResponse
import datetime
from django.db import connection
from wisccc.models import (
    Researcher,
    SurveyFarm,
    SurveyField,
    FieldFarm,
    AncillaryData,
    Farmer,
    SurveyRegistration,
)
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

from django.contrib.auth.models import User
from django.conf import settings
import os


def get_registration_download():
    survey_registrants = (
        SurveyRegistration.objects.all()
        .select_related("farmer")
        .select_related("farmer__user")
    )

    df = pd.DataFrame(
        list(
            survey_registrants.values_list(
                # From registration
                "signup_timestamp",
                # From Farmer
                "farmer__id",
                # From User
                "farmer__user__email",
                "farmer__user__username",
                # From Farmer
                "farmer__first_name",
                "farmer__last_name",
                "farmer__farm_name",
                "farmer__county",
                "farmer__address_street",
                "farmer__address_municipality",
                "farmer__address_state",
                "farmer__address_zipcode",
                "farmer__phone_number",
                # From registration
                "survey_year",
                "biomass_or_just_survey",
                "do_you_have_a_biomas_kit",
                "do_you_need_assistance",
                "howd_you_hear",
                "belong_to_groups",
                "notes",
            )
        ),
        columns=[
            # From registration
            "signup_timestamp",
            # From Farmer
            "id",
            # From User
            "email",
            "username",
            # From Farmer
            "first_name",
            "last_name",
            "farm_name",
            "county",
            "street",
            "municipality",
            "state",
            "zipcode",
            "phone_number",
            # From registrants
            "survey_year",
            "biomass_or_just_survey",
            "do_you_have_a_biomas_kit",
            "do_you_need_assistance",
            "howd_you_hear",
            "belong_to_groups",
            "notes",
        ],
    )
    # convert farmer id to string, convert survey_year to string
    #   grab just the year and create and id
    # Add -F for fall sampling
    df["id"] = (
        df["id"].apply(str).str.zfill(5)
        + "-"
        + df["survey_year"].apply(str).str[-2:]
        + "-F"
    )
    df = df.drop("survey_year", axis=1)
    return df


def get_researchers_download():
    """For gathering and formating the data for downloading a list of
    collaborating researchers"""
    researchers = Researcher.objects.all().select_related("user")

    df = pd.DataFrame(
        list(
            researchers.values_list(
                # From Researcher
                "signup_timestamp",
                # From User
                "user__email",
                "user__username",
                # From Researcher
                "first_name",
                "last_name",
                "institution",
                "agreement_doc",
                "notes",
                "download_count",
                "last_download_timestamp",
                "approved",
                "approved_date",
            )
        ),
        columns=[
            # From Researcher
            "signup_timestamp",
            # From User
            "email",
            "username",
            # From Researcher
            "first_name",
            "last_name",
            "institution",
            "agreement_doc",
            "notes",
            "download_count",
            "last_download_timestamp",
            "approved",
            "approved_date",
        ],
    )

    return df


def convert_to_human_readable(column, choices_object):
    """Takes a column and a choices objects and converts it to
    the human readable format"""
    dict_choices = dict(choices_object.choices)
    try:
        new_version = dict_choices[column]
    except KeyError as e:
        new_version = column

    return new_version


def get_survey_data():
    """For creating a pandas dataframe for ALL survey data"""

    survey_fields = (
        SurveyField.objects.all()
        .select_related("survey_farm")
        .select_related("field_farm")
        .select_related("survey_farm__farmer")
        .select_related("survey_farm__farmer__user")
    )

    ancillary_data = AncillaryData.objects.all()

    dct_choices = {
        "info_source_nutrient_mgmt_1": NutrientMgmtSourcesChoices,
        "info_source_nutrient_mgmt_2": NutrientMgmtSourcesChoices,
        "info_source_nutrient_mgmt_3": NutrientMgmtSourcesChoices,
        "info_source_cover_crops_1": CoverCropInfoSourcesChoices,
        "info_source_cover_crops_2": CoverCropInfoSourcesChoices,
        "info_source_cover_crops_3": CoverCropInfoSourcesChoices,
        "support_cover_crops_1": CoverCropSupportChoices,
        "two_years_ago_cover_crop_species": CoverCropChoices,
        "two_years_ago_cash_crop_species": CashCropChoices,
        "last_years_cover_crop_species": CoverCropChoices,
        "last_years_cash_crop_species": CashCropChoices,
        "this_years_cover_crop_species": CoverCropChoices,
        "this_years_cash_crop_species": CashCropChoices,
        "cover_crop_species_1": CoverCropChoices,
        "cover_crop_species_2": CoverCropChoices,
        "cover_crop_species_3": CoverCropChoices,
        "cover_crop_species_4": CoverCropChoices,
        "cover_crop_species_5": CoverCropChoices,
        "cover_crop_planting_rate_1_units": CoverCropRateUnitsChoices,
        "cover_crop_planting_rate_2_units": CoverCropRateUnitsChoices,
        "cover_crop_planting_rate_3_units": CoverCropRateUnitsChoices,
        "cover_crop_planting_rate_4_units": CoverCropRateUnitsChoices,
        "cover_crop_planting_rate_5_units": CoverCropRateUnitsChoices,
        "dominant_soil_texture": SoilTextureClassChoices,
        "manure_prior_rate_units": ManureApplicateUnitsChoices,
        "manure_post_rate_units": ManureApplicateUnitsChoices,
        "tillage_system_cash_crop": TillageSystemChoices,
        "primary_tillage_equipment": PrimaryTillageEquipmentChoices,
        "secondary_tillage_equipment": SecondaryTillageEquipmentChoices,
        "soil_conditions_at_cover_crop_seeding": SoilConditionsSeedingChoices,
        "cover_crop_seeding_method": SeedingMethodChoices,
        "cover_crop_estimated_termination": TerminationMethodTimingChoices,
    }
    # Any column added here will need to have its name added in the below list!
    df = pd.DataFrame(
        list(
            survey_fields.values_list(
                # From User
                "survey_farm__farmer__user__username",
                "survey_farm__farmer__user__email",
                # From Farmer
                "survey_farm__farmer__first_name",
                "survey_farm__farmer__last_name",
                "survey_farm__farmer__farm_name",
                "survey_farm__farmer__county",
                # From SurveyFarm
                "survey_farm__id",
                "survey_farm__survey_created",
                "survey_farm__last_updated",
                "survey_farm__survey_year",
                "survey_farm__notes_admin",
                "survey_farm__confirmed_accurate",
                "survey_farm__years_experience",
                "survey_farm__main_cc_goal_this_year",
                "survey_farm__satisfied_with_cc_results",
                "survey_farm__biggest_challenge_cc",
                "survey_farm__learning_history_cc",
                "survey_farm__conservation_programs",
                "survey_farm__total_acres",
                "survey_farm__percent_of_farm_cc",
                "survey_farm__dominant_soil_series_1",
                "survey_farm__dominant_soil_series_2",
                "survey_farm__dominant_soil_series_3",
                "survey_farm__dominant_soil_series_4",
                "survey_farm__info_source_nutrient_mgmt_1",
                "survey_farm__info_source_nutrient_mgmt_2",
                "survey_farm__info_source_nutrient_mgmt_3",
                "survey_farm__source_nutrient_mgmt_write_in",
                "survey_farm__cov_crops_for_ntrnt_mgmt_comments_questions",
                "survey_farm__info_source_cover_crops_1",
                "survey_farm__info_source_cover_crops_2",
                "survey_farm__info_source_cover_crops_3",
                "survey_farm__info_source_cover_crops_write_in",
                "survey_farm__support_cover_crops_1",
                "survey_farm__support_cover_crops_write_in",
                "survey_farm__lacking_any_info_cover_crops",
                "survey_farm__barriers_to_expansion",
                "survey_farm__barriers_to_expansion_write_in",
                "survey_farm__quit_planting_cover_crops",
                "survey_farm__if_use_crop_insurance",
                "survey_farm__why_cover_crops_write_in",
                "survey_farm__cover_crops_delay_cash_crop",
                "survey_farm__save_cover_crop_seed",
                "survey_farm__source_cover_crop_seed",
                "survey_farm__interesting_tales",
                "survey_farm__where_to_start",
                "survey_farm__additional_thoughts",
                "survey_farm__encourage_cc",
                "survey_farm__encourage_cc_write_in",
                # From SurveyField
                "id",
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
                "cover_crop_multispecies_mix_write_in",
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
                "cover_crop_estimated_termination_write_in",
                "days_between_crop_hvst_and_cc_estd",
                "derived_species_class",
                # From FieldFarm
                "field_farm__closest_zip_code",
                "field_farm__field_acreage",
                "field_farm__field_location",
                "field_farm__derived_county",
            )
        ),
        columns=[
            # From User
            "username",
            "email",
            # From Farmer
            "first_name",
            "last_name",
            "farm_name",
            "county",
            # From SurveyFarm
            "survey_farm_id",
            "survey_created",
            "last_updated",
            "survey_year",
            "notes_admin_farm",
            "confirmed_accurate",
            "years_experience",
            "main_cc_goal_this_year",
            "satisfied_with_cc_results",
            "biggest_challenge_cc",
            "learning_history_cc",
            "conservation_programs",
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
            # From SurveyField
            "survey_field_id",
            "crop_rotation",
            "two_years_ago_cover_crop_species",
            "two_years_ago_cash_crop_species",
            "last_years_cover_crop_species",
            "last_years_cash_crop_species",
            "this_years_cover_crop_species",
            "this_years_cash_crop_species",
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
            "cover_crop_estimated_termination_write_in",
            "days_between_crop_hvst_and_cc_estd",
            "derived_species_class",
            # From FieldFarm
            "closest_zip_code",
            "field_acreage",
            "field_location",
            "derived_county",
        ],
    )

    df_anc = pd.DataFrame(
        list(
            ancillary_data.values_list(
                # From Ancillary Data
                "survey_field_id",
                "biomass_collection_date",
                "cp",
                "andf",
                "undfom30",
                "ndfd30",
                "tdn_adf",
                "milk_ton_milk2013",
                "rfq",
                "undfom240",
                "dry_matter",
                "rfv",
                "cc_biomass",
                "total_nitrogen",
                
                "percent_p",
                "percent_k",
                "percent_ca",
                "percent_mg",
                "percent_s",
                "c_to_n_ratio",

                "n_content",
                "p_content",
                "k_content",
                "ca_content",
                "mg_content",
                "s_content",
                "c_content",

                "height_of_stand",
                "acc_gdd",
                "total_precip",

                "precip_preplant_3_wk",
                "precip_preplant_2_wk",
                "precip_preplant_1_wk",
                "precip_postplant_1_wk",
                "precip_postplant_2_wk",
                "precip_postplant_3_wk",        

                "spring_biomass_collection_date",
                "spring_cp",
                "spring_andf",
                "spring_undfom30",
                "spring_ndfd30",
                "spring_tdn_adf",
                "spring_milk_ton_milk2013",
                "spring_rfq",
                "spring_undfom240",
                "spring_dry_matter",
                "spring_rfv",
                "spring_cc_biomass",
                "spring_total_nitrogen",

                "spring_percent_p",
                "spring_percent_k",
                "spring_percent_ca",
                "spring_percent_mg",
                "spring_percent_s",
                "spring_c_to_n_ratio",

                "spring_n_content",
                "spring_p_content",
                "spring_k_content",
                "spring_ca_content",
                "spring_mg_content",
                "spring_s_content",
                "spring_c_content",

                "spring_height_of_stand",
                "spring_acc_gdd",
                "spring_total_precip",
                "notes_admin",
            )
        ),
        columns=[
            # From Ancillary Data
            "survey_field_id",
            "biomass_collection_date_fall",
            "cp_fall",
            "andf_fall",
            "undfom30_fall",
            "ndfd30_fall",
            "tdn_adf_fall",
            "milk_ton_milk2013_fall",
            "rfq_fall",
            "undfom240_fall",
            "dry_matter_fall",
            "rfv_fall",
            "cc_biomass_fall",
            "total_nitrogen_fall",

            "percent_p_fall",
            "percent_k_fall",
            "percent_ca_fall",
            "percent_mg_fall",
            "percent_s_fall",
            "c_to_n_ratio_fall",

            "n_content_fall",
            "p_content_fall",
            "k_content_fall",
            "ca_content_fall",
            "mg_content_fall",
            "s_content_fall",
            "c_content_fall",

            "height_of_stand_fall",
            "acc_gdd_fall",
            "total_precip_fall",
            "precip_preplant_3_wk",
            "precip_preplant_2_wk",
            "precip_preplant_1_wk",
            "precip_postplant_1_wk",
            "precip_postplant_2_wk",
            "precip_postplant_3_wk",            
            "biomass_collection_date_spring",
            "cp_spring",
            "andf_spring",
            "undfom30_spring",
            "ndfd30_spring",
            "tdn_adf_spring",
            "milk_ton_milk2013_spring",
            "rfq_spring",
            "undfom240_spring",
            "dry_matter_spring",
            "rfv_spring",
            "cc_biomass_spring",
            "total_nitrogen_spring",

            "percent_p_spring",
            "percent_k_spring",
            "percent_ca_spring",
            "percent_mg_spring",
            "percent_s_spring",
            "c_to_n_ratio_spring",

            "n_content_spring",
            "p_content_spring",
            "k_content_spring",
            "ca_content_spring",
            "mg_content_spring",
            "s_content_spring",
            "c_content_spring",

            "height_of_stand_spring",
            "acc_gdd_spring",
            "total_precip_spring",
            "notes_admin_lab_data",
        ],
    )

    df = df.merge(
        df_anc, how="left", left_on="survey_field_id", right_on="survey_field_id"
    )

    for col in dct_choices:
        df[col] = df[col].apply(convert_to_human_readable, args=(dct_choices[col],))

    # For creating concat of cc species
    cols_species = ['cover_crop_species_1', 'cover_crop_species_2', "cover_crop_species_3", "cover_crop_species_4", "cover_crop_species_5"]
    df['cc_species_raw'] = df[cols_species].fillna('').agg(','.join, axis=1)
    df.cc_species_raw = df.cc_species_raw.str.replace(r",+$", "")
    return df


def pull_all_years_together(f_output):
    """f_output is format of the output:
    sql: for returning just the query
    json: for returning json
    df: for pandas dataframe
    table: for creating 'wisc_cc_all_together' in db;
        for testing purposes.
    """

    query = """
 

	SELECT 
		prevsurv.survey_farm_id as farm_id
        , prevsurv.survey_field_id as survey_field_id
        , prevsurv.survey_field_id as id
        , stat.year
        , stat.county
        , stat.county_single
        , stat.years_experience
        , stat.zipcode
        , stat.previous_crop
        , stat.cash_crop_planting_date 
        , stat.dominant_soil_texture
        , stat.manure_prior 
        , null as manure_prior_rate
        , null as manure_prior_rate_units
        , stat.manure_post
        , null manure_post_rate
        , null as manure_post_rate_units
        , stat.manure_rate 
        , stat.manure_value 
        , stat.tillage_system 
        , stat.tillage_equip_primary
        , stat.tillage_equip_secondary
        , stat.residue_remaining
        , stat.soil_conditions
        , stat.cc_seeding_method
        , stat.cc_planting_rate
        , stat.cc_termination
        , stat.days_between_crop_hvst_and_cc_estd
        , stat.site_lon
        , stat.site_lat        
        , stat.cc_planting_date
        
        , stat.anpp
        , stat.cc_biomass_collection_date
        , stat.total_precip
        , stat.acc_gdd
        , stat.days_from_plant_to_bio_hrvst

        , stat.precip_preplant_3_wk
        , stat.precip_preplant_2_wk
        , stat.precip_preplant_1_wk
        , stat.precip_postplant_1_wk
        , stat.precip_postplant_2_wk
        , stat.precip_postplant_3_wk        

        , stat.field_acreage as field_acreage
        , stat.years_with_cover_crops as years_with_cover_crops
        , stat.cover_crop_planting_cost as cover_crop_planting_cost
        , stat.cover_crop_seed_cost as cover_crop_seed_cost
        
        , stat.cc_biomass
        , stat.fq_cp
        , stat.fq_andf
        , stat.fq_undfom30
        , stat.fq_ndfd30
        , stat.fq_tdn_adf
        , stat.fq_milkton
        , stat.fq_rfq
        , stat.fq_undfom240
        , stat.fq_dry_matter
        , stat.fq_adf
        , stat.fq_rfv        
        , stat.fq_total_nitrogen as total_nitrogen

        , stat.fq_total_phosphorus as percent_p
        , stat.fq_total_potassium as percent_k
        , stat.fq_total_calcium as percent_ca
        , stat.fq_total_magnesium as percent_mg
        , stat.fq_total_sulfur as percent_s
        , stat.fq_c_to_n_ratio as c_to_n_ratio

        , stat.fq_nitrogen_content as n_content
        , stat.fq_phosphorus_content as p_content
        , stat.fq_potassium_content as k_content
        , stat.fq_calcium_content as ca_content
        , stat.fq_magnesium_content as mg_content
        , stat.fq_sulfur_content as s_content
        , stat.fq_carbon_content as c_content

        , null as height_of_stand
        , null as fall_notes
        , null as spring_cc_biomass_collection_date
        , null as spring_total_precip
        , null as spring_acc_gdd        
        , null as spring_cc_biomass
        , null as spring_fq_cp
        , null as spring_fq_andf
        , null as spring_fq_undfom30
        , null as spring_fq_ndfd30
        , null as spring_fq_tdn_adf
        , null as spring_fq_milkton
        , null as spring_fq_rfq
        , null as spring_fq_undfom240
        , null as spring_fq_dry_matter
        , null as spring_fq_adf
        , null as spring_fq_rfv

        , null as spring_total_nitrogen        

        , null as spring_percent_p
        , null as spring_percent_k
        , null as spring_percent_ca
        , null as spring_percent_mg
        , null as spring_percent_s
        , null as spring_c_to_n_ratio

        , null as spring_n_content
        , null as spring_p_content
        , null as spring_k_content
        , null as spring_ca_content
        , null as spring_mg_content
        , null as spring_s_content
        , null as spring_c_content
        
        , null as spring_height_of_stand
        , null as spring_notes
        , stat.cc_rate_and_species
        , stat.cc_species
        , stat.cc_species_raw
        , null as survey_response_id
        
    from wisc_cc as stat
    inner join
  	(
        select
            wsf.id as survey_farm_id,
            wsfld.id as survey_field_id,
            split_part(notes_admin, ';', 1) as mrill_id
        from wisccc_surveyfarm as wsf
        left join wisccc_surveyfield as wsfld
        on wsf.id = wsfld.survey_farm_id
        where survey_year < 2023      
    ) as prevsurv
	on stat.id = prevsurv.mrill_id

    union all

    select
        a.master_survey_farm_id as farm_id,
        surveyfield_id as survey_field_id,
        surveyfield_id as id,
        year,
        a.county,
        derived_county as county_single,
        years_experience::text as years_experience,
        closest_zip_code as zipcode,
        mod_crop_rotation_2023_cash_crop_species as previous_crop,
        cash_crop_planting_date::timestamp,
        lower(replace(dominant_soil_texture, '_', ' ')) as dominant_soil_texture,
        -- Make this yes no? Or change static to boolean?
        case
            when manure_prior = 'true' then 'Yes'
            when manure_prior = 'false' then 'No'
            when manure_prior is null then 'No'
        end as manure_prior,
        manure_prior_rate,
        mod_manure_prior_rate_units as manure_prior_rate_units,
        case
            when manure_post = 'true' then 'Yes'
            when manure_post = 'false' then 'No'
            when manure_post is null then 'No'
        end as manure_post,
        manure_post_rate,
        mod_manure_post_rate_units as mod_manure_post_rate_units,	
        null as manure_rate, 
        null as manure_value, 	
        mod_tillage_system_cash_crop as tillage_system,
        primary_tillage_equipment as tillage_equip_primary,
        secondary_tillage_equipment as tillage_equip_secondary,
        mod_residue_remaining as residue_remaining,	
        lower(soil_conditions_at_cover_crop_seeding) as soil_conditions,
        mod_cc_seeding_method as cc_seeding_method,
        concat(		
            concat(  cover_crop_planting_rate_1, ' ', mod_cover_crop_planting_rate_1_units, ' ', mod_cover_crop_species_1),
            nullif(concat(  ', ', cover_crop_planting_rate_2, ' ', mod_cover_crop_planting_rate_2_units, ' ', mod_cover_crop_species_2), ',   '),
            nullif(concat(  ', ', cover_crop_planting_rate_3, ' ', mod_cover_crop_planting_rate_3_units, ' ', mod_cover_crop_species_3), ',   '),
            nullif(concat(  ', ', cover_crop_planting_rate_4, ' ', mod_cover_crop_planting_rate_4_units, ' ', mod_cover_crop_species_4), ',   '),
            nullif(concat(  ', ', cover_crop_planting_rate_5, ' ', mod_cover_crop_planting_rate_5_units, ' ', mod_cover_crop_species_5), ',   ')
        ) as cc_planting_rate,
        mod_cover_crop_estimated_termination as cc_termination,
        days_between_crop_hvst_and_cc_estd as days_between_crop_hvst_and_cc_estd,
	    ST_X(field_location) as site_lon,
	    ST_Y(field_location) as site_lat,                
        cover_crop_planting_date::timestamp as cc_planting_date,
        
        null as anpp,
        biomass_collection_date as cc_biomass_collection_date,
        total_precip as total_precip,
        acc_gdd as acc_gdd,
        null as days_from_plant_to_bio_hrvst,

        precip_preplant_3_wk, 
        precip_preplant_2_wk,
        precip_preplant_1_wk,
        precip_postplant_1_wk,
        precip_postplant_2_wk,
        precip_postplant_3_wk,               

        field_acreage as field_acreage, 
        years_with_cover_crops as years_with_cover_crops, 
        cover_crop_planting_cost as cover_crop_planting_cost, 
        cover_crop_seed_cost as cover_crop_seed_cost, 
        
        cc_biomass,
        cp as fq_cp,
        andf as fq_andf,
        undfom30 as fq_undfom30,
        ndfd30 as fq_ndfd30,
        tdn_adf as fq_tdn_adf,
        milk_ton_milk2013 as fq_milkton,
        rfq as fq_rfq,
        undfom240 as fq_undfom240,
        dry_matter as fq_dry_matter,
        adf as fq_adf,
        rfv as fq_rfv,                
        total_nitrogen as total_nitrogen,

        percent_p,
        percent_k,
        percent_ca,
        percent_mg,
        percent_s,
        c_to_n_ratio,

        n_content,
        p_content,
        k_content,
        ca_content,
        mg_content,
        s_content,
        c_content,

        height_of_stand,
        fall_notes,
        spring_biomass_collection_date as spring_cc_biomass_collection_date,
        spring_total_precip as spring_total_precip,
        spring_acc_gdd as spring_acc_gdd,    
        spring_cc_biomass as spring_cc_biomass,
        spring_cp as spring_fq_cp,
        spring_andf as spring_fq_andf,
        spring_undfom30 as spring_fq_undfom30,
        spring_ndfd30 as spring_fq_ndfd30,
        spring_tdn_adf as spring_fq_tdn_adf,
        spring_milk_ton_milk2013 as spring_fq_milkton,
        spring_rfq as spring_fq_rfq,
        spring_undfom240 as spring_fq_undfom240,
        spring_dry_matter as spring_fq_dry_matter,
        spring_adf as spring_fq_adf,
        spring_rfv as spring_fq_rfv,
        spring_total_nitrogen as spring_total_nitrogen,

        spring_percent_p,
        spring_percent_k,
        spring_percent_ca,
        spring_percent_mg,
        spring_percent_s,
        spring_c_to_n_ratio,

        spring_n_content,
        spring_p_content,
        spring_k_content,
        spring_ca_content,
        spring_mg_content,
        spring_s_content,
        spring_c_content,

        spring_height_of_stand,
        spring_notes,
        
        concat(		
            concat(  cover_crop_planting_rate_1, ' ', mod_cover_crop_planting_rate_1_units, ' ', mod_cover_crop_species_1),
            nullif(concat(  ', ', cover_crop_planting_rate_2, ' ', mod_cover_crop_planting_rate_2_units, ' ', mod_cover_crop_species_2), ',   '),
            nullif(concat(  ', ', cover_crop_planting_rate_3, ' ', mod_cover_crop_planting_rate_3_units, ' ', mod_cover_crop_species_3), ',   '),
            nullif(concat(  ', ', cover_crop_planting_rate_4, ' ', mod_cover_crop_planting_rate_4_units, ' ', mod_cover_crop_species_4), ',   '),
            nullif(concat(  ', ', cover_crop_planting_rate_5, ' ', mod_cover_crop_planting_rate_5_units, ' ', mod_cover_crop_species_5), ',   ')
        ) as cc_rate_and_species,
        derived_species_class as cc_species,		
        concat(
            mod_cover_crop_species_1, 
            nullif(concat(', ', mod_cover_crop_species_2), ', '), 
            nullif(concat(', ', mod_cover_crop_species_3), ', '), 
            nullif(concat(', ', mod_cover_crop_species_4), ', '), 
            nullif(concat(', ', mod_cover_crop_species_5), ', ')
        ) as cc_species_raw,
        survey_response_id
    from (
        select
            surveyfield.*,
            surveyfarm.*,
            fieldfarm.*,
            farmer.*,
            ancil.*,
            concat(
                fieldfarm.closest_zip_code,
                '-',
                upper(substring(farmer.first_name, 1, 1)),
                upper(substring(farmer.last_name,  1, 1)),
                '-',
                substring(survey_year::text, 3,4)
            ) as wisc_cc_id,
            surveyfarm.survey_year as year,
            surveyfarm.id as master_survey_farm_id,
            surveyfield.id as surveyfield_id,
            case
                when surveyfield.cover_crop_species_1 = 'ANNUAL_RYEGRASS' then 'annual ryegrass'
                when surveyfield.cover_crop_species_1 = 'BALANSA_CLOVER' then 'balansa clover'
                when surveyfield.cover_crop_species_1 = 'BARLEY' then 'barley'
                when surveyfield.cover_crop_species_1 = 'BERSEEM_CLOVER' then 'berseem clover'
                when surveyfield.cover_crop_species_1 = 'BUCKWHEAT' then 'buckwheat'

                when surveyfield.cover_crop_species_1 = 'CANOLA' then 'canola/rapeseed'
                when surveyfield.cover_crop_species_1 = 'CEREAL_RYE' then 'cereal (winter) rye'
                when surveyfield.cover_crop_species_1 = 'COWPEA' then 'cowpea'
                when surveyfield.cover_crop_species_1 = 'CRIMSON_CLOVER' then 'crimson clover'
                when surveyfield.cover_crop_species_1 = 'DUTCH_WHITE_CLOVER' then 'Dutch white clover'

                when surveyfield.cover_crop_species_1 = 'FIELD_PEA' then 'field/forage pea'
                when surveyfield.cover_crop_species_1 = 'FLAX' then 'flax'
                when surveyfield.cover_crop_species_1 = 'HAIRY_VETCH' then 'hairy vetch'
                when surveyfield.cover_crop_species_1 = 'KALE' then 'kale'
                when surveyfield.cover_crop_species_1 = 'MILLET' then 'millet'

                when surveyfield.cover_crop_species_1 = 'OATS' then 'oats'
                when surveyfield.cover_crop_species_1 = 'OTHER_LEGUME' then 'other (legume)'
                when surveyfield.cover_crop_species_1 = 'OTHER_GRASS' then 'other (grass)'
                when surveyfield.cover_crop_species_1 = 'OTHER_BROADLEAF' then 'other (broadleaf)'
                when surveyfield.cover_crop_species_1 = 'PLANTAIN' then 'plantain'


                when surveyfield.cover_crop_species_1 = 'RADISH' then 'radish'  
                when surveyfield.cover_crop_species_1 = 'RED_CLOVER' then 'red clover'
                when surveyfield.cover_crop_species_1 = 'SORGHUM' then 'sorghum'
                when surveyfield.cover_crop_species_1 = 'SORGHUM_SUDAN' then 'sorghum-sudan'
                when surveyfield.cover_crop_species_1 = 'SOYBEANS' then 'soybeans'

                when surveyfield.cover_crop_species_1 = 'SUNFLOWER' then 'sunflower'
                when surveyfield.cover_crop_species_1 = 'SUN_HEMP' then 'sun hemp'
                when surveyfield.cover_crop_species_1 = 'TRITICALE' then 'triticale'
                when surveyfield.cover_crop_species_1 = 'TURNIP' then 'turnip'
                when surveyfield.cover_crop_species_1 = 'WHEAT_SPRING' then 'wheat (spring)'

                when surveyfield.cover_crop_species_1 = 'WHEAT_WINTER' then 'wheat (winter)'
                when surveyfield.cover_crop_species_1 = 'WINTER_PEA' then 'winter pea'
                when surveyfield.cover_crop_species_1 = 'YELLOW_SWEET_CLOVER' then 'yellow sweet clover'
                when surveyfield.cover_crop_species_1 = 'MULITSPECIES' then 'multispecies mix of 2 or more'
                when surveyfield.cover_crop_species_1 = 'OTHER' then 'other'		

            end as mod_cover_crop_species_1,
            case
                when surveyfield.cover_crop_species_2 = 'ANNUAL_RYEGRASS' then 'annual ryegrass'
                when surveyfield.cover_crop_species_2 = 'BALANSA_CLOVER' then 'balansa clover'
                when surveyfield.cover_crop_species_2 = 'BARLEY' then 'barley'
                when surveyfield.cover_crop_species_2 = 'BERSEEM_CLOVER' then 'berseem clover'
                when surveyfield.cover_crop_species_2 = 'BUCKWHEAT' then 'buckwheat'

                when surveyfield.cover_crop_species_2 = 'CANOLA' then 'canola/rapeseed'
                when surveyfield.cover_crop_species_2 = 'CEREAL_RYE' then 'cereal (winter) rye'
                when surveyfield.cover_crop_species_2 = 'COWPEA' then 'cowpea'
                when surveyfield.cover_crop_species_2 = 'CRIMSON_CLOVER' then 'crimson clover'
                when surveyfield.cover_crop_species_2 = 'DUTCH_WHITE_CLOVER' then 'Dutch white clover'

                when surveyfield.cover_crop_species_2 = 'FIELD_PEA' then 'field/forage pea'
                when surveyfield.cover_crop_species_2 = 'FLAX' then 'flax'
                when surveyfield.cover_crop_species_2 = 'HAIRY_VETCH' then 'hairy vetch'
                when surveyfield.cover_crop_species_2 = 'KALE' then 'kale'
                when surveyfield.cover_crop_species_2 = 'MILLET' then 'millet'

                when surveyfield.cover_crop_species_2 = 'OATS' then 'oats'
                when surveyfield.cover_crop_species_2 = 'OTHER_LEGUME' then 'other (legume)'
                when surveyfield.cover_crop_species_2 = 'OTHER_GRASS' then 'other (grass)'
                when surveyfield.cover_crop_species_2 = 'OTHER_BROADLEAF' then 'other (broadleaf)'
                when surveyfield.cover_crop_species_2 = 'PLANTAIN' then 'plantain'


                when surveyfield.cover_crop_species_2 = 'RADISH' then 'radish'  
                when surveyfield.cover_crop_species_2 = 'RED_CLOVER' then 'red clover'
                when surveyfield.cover_crop_species_2 = 'SORGHUM' then 'sorghum'
                when surveyfield.cover_crop_species_2 = 'SORGHUM_SUDAN' then 'sorghum-sudan'
                when surveyfield.cover_crop_species_2 = 'SOYBEANS' then 'soybeans'

                when surveyfield.cover_crop_species_2 = 'SUNFLOWER' then 'sunflower'
                when surveyfield.cover_crop_species_2 = 'SUN_HEMP' then 'sun hemp'
                when surveyfield.cover_crop_species_2 = 'TRITICALE' then 'triticale'
                when surveyfield.cover_crop_species_2 = 'TURNIP' then 'turnip'
                when surveyfield.cover_crop_species_2 = 'WHEAT_SPRING' then 'wheat (spring)'

                when surveyfield.cover_crop_species_2 = 'WHEAT_WINTER' then 'wheat (winter)'
                when surveyfield.cover_crop_species_2 = 'WINTER_PEA' then 'winter pea'
                when surveyfield.cover_crop_species_2 = 'YELLOW_SWEET_CLOVER' then 'yellow sweet clover'
                when surveyfield.cover_crop_species_2 = 'MULITSPECIES' then 'multispecies mix of 2 or more'
                when surveyfield.cover_crop_species_2 = 'OTHER' then 'other'	
            end as mod_cover_crop_species_2,
            case
                when surveyfield.cover_crop_species_3 = 'ANNUAL_RYEGRASS' then 'annual ryegrass'
                when surveyfield.cover_crop_species_3 = 'BALANSA_CLOVER' then 'balansa clover'
                when surveyfield.cover_crop_species_3 = 'BARLEY' then 'barley'
                when surveyfield.cover_crop_species_3 = 'BERSEEM_CLOVER' then 'berseem clover'
                when surveyfield.cover_crop_species_3 = 'BUCKWHEAT' then 'buckwheat'

                when surveyfield.cover_crop_species_3 = 'CANOLA' then 'canola/rapeseed'
                when surveyfield.cover_crop_species_3 = 'CEREAL_RYE' then 'cereal (winter) rye'
                when surveyfield.cover_crop_species_3 = 'COWPEA' then 'cowpea'
                when surveyfield.cover_crop_species_3 = 'CRIMSON_CLOVER' then 'crimson clover'
                when surveyfield.cover_crop_species_3 = 'DUTCH_WHITE_CLOVER' then 'Dutch white clover'

                when surveyfield.cover_crop_species_3 = 'FIELD_PEA' then 'field/forage pea'
                when surveyfield.cover_crop_species_3 = 'FLAX' then 'flax'
                when surveyfield.cover_crop_species_3 = 'HAIRY_VETCH' then 'hairy vetch'
                when surveyfield.cover_crop_species_3 = 'KALE' then 'kale'
                when surveyfield.cover_crop_species_3 = 'MILLET' then 'millet'

                when surveyfield.cover_crop_species_3 = 'OATS' then 'oats'
                when surveyfield.cover_crop_species_3 = 'OTHER_LEGUME' then 'other (legume)'
                when surveyfield.cover_crop_species_3 = 'OTHER_GRASS' then 'other (grass)'
                when surveyfield.cover_crop_species_3 = 'OTHER_BROADLEAF' then 'other (broadleaf)'
                when surveyfield.cover_crop_species_3 = 'PLANTAIN' then 'plantain'


                when surveyfield.cover_crop_species_3 = 'RADISH' then 'radish'  
                when surveyfield.cover_crop_species_3 = 'RED_CLOVER' then 'red clover'
                when surveyfield.cover_crop_species_3 = 'SORGHUM' then 'sorghum'
                when surveyfield.cover_crop_species_3 = 'SORGHUM_SUDAN' then 'sorghum-sudan'
                when surveyfield.cover_crop_species_3 = 'SOYBEANS' then 'soybeans'

                when surveyfield.cover_crop_species_3 = 'SUNFLOWER' then 'sunflower'
                when surveyfield.cover_crop_species_3 = 'SUN_HEMP' then 'sun hemp'
                when surveyfield.cover_crop_species_3 = 'TRITICALE' then 'triticale'
                when surveyfield.cover_crop_species_3 = 'TURNIP' then 'turnip'
                when surveyfield.cover_crop_species_3 = 'WHEAT_SPRING' then 'wheat (spring)'

                when surveyfield.cover_crop_species_3 = 'WHEAT_WINTER' then 'wheat (winter)'
                when surveyfield.cover_crop_species_3 = 'WINTER_PEA' then 'winter pea'
                when surveyfield.cover_crop_species_3 = 'YELLOW_SWEET_CLOVER' then 'yellow sweet clover'
                when surveyfield.cover_crop_species_3 = 'MULITSPECIES' then 'multispecies mix of 2 or more'
                when surveyfield.cover_crop_species_3 = 'OTHER' then 'other'	
            end as mod_cover_crop_species_3,
            case
                when surveyfield.cover_crop_species_4 = 'ANNUAL_RYEGRASS' then 'annual ryegrass'
                when surveyfield.cover_crop_species_4 = 'BALANSA_CLOVER' then 'balansa clover'
                when surveyfield.cover_crop_species_4 = 'BARLEY' then 'barley'
                when surveyfield.cover_crop_species_4 = 'BERSEEM_CLOVER' then 'berseem clover'
                when surveyfield.cover_crop_species_4 = 'BUCKWHEAT' then 'buckwheat'

                when surveyfield.cover_crop_species_4 = 'CANOLA' then 'canola/rapeseed'
                when surveyfield.cover_crop_species_4 = 'CEREAL_RYE' then 'cereal (winter) rye'
                when surveyfield.cover_crop_species_4 = 'COWPEA' then 'cowpea'
                when surveyfield.cover_crop_species_4 = 'CRIMSON_CLOVER' then 'crimson clover'
                when surveyfield.cover_crop_species_4 = 'DUTCH_WHITE_CLOVER' then 'Dutch white clover'

                when surveyfield.cover_crop_species_4 = 'FIELD_PEA' then 'field/forage pea'
                when surveyfield.cover_crop_species_4 = 'FLAX' then 'flax'
                when surveyfield.cover_crop_species_4 = 'HAIRY_VETCH' then 'hairy vetch'
                when surveyfield.cover_crop_species_4 = 'KALE' then 'kale'
                when surveyfield.cover_crop_species_4 = 'MILLET' then 'millet'

                when surveyfield.cover_crop_species_4 = 'OATS' then 'oats'
                when surveyfield.cover_crop_species_4 = 'OTHER_LEGUME' then 'other (legume)'
                when surveyfield.cover_crop_species_4 = 'OTHER_GRASS' then 'other (grass)'
                when surveyfield.cover_crop_species_4 = 'OTHER_BROADLEAF' then 'other (broadleaf)'
                when surveyfield.cover_crop_species_4 = 'PLANTAIN' then 'plantain'


                when surveyfield.cover_crop_species_4 = 'RADISH' then 'radish'  
                when surveyfield.cover_crop_species_4 = 'RED_CLOVER' then 'red clover'
                when surveyfield.cover_crop_species_4 = 'SORGHUM' then 'sorghum'
                when surveyfield.cover_crop_species_4 = 'SORGHUM_SUDAN' then 'sorghum-sudan'
                when surveyfield.cover_crop_species_4 = 'SOYBEANS' then 'soybeans'

                when surveyfield.cover_crop_species_4 = 'SUNFLOWER' then 'sunflower'
                when surveyfield.cover_crop_species_4 = 'SUN_HEMP' then 'sun hemp'
                when surveyfield.cover_crop_species_4 = 'TRITICALE' then 'triticale'
                when surveyfield.cover_crop_species_4 = 'TURNIP' then 'turnip'
                when surveyfield.cover_crop_species_4 = 'WHEAT_SPRING' then 'wheat (spring)'

                when surveyfield.cover_crop_species_4 = 'WHEAT_WINTER' then 'wheat (winter)'
                when surveyfield.cover_crop_species_4 = 'WINTER_PEA' then 'winter pea'
                when surveyfield.cover_crop_species_4 = 'YELLOW_SWEET_CLOVER' then 'yellow sweet clover'
                when surveyfield.cover_crop_species_4 = 'MULITSPECIES' then 'multispecies mix of 2 or more'
                when surveyfield.cover_crop_species_4 = 'OTHER' then 'other'	
            end as mod_cover_crop_species_4,
            case
                when surveyfield.cover_crop_species_5 = 'ANNUAL_RYEGRASS' then 'annual ryegrass'
                when surveyfield.cover_crop_species_5 = 'BALANSA_CLOVER' then 'balansa clover'
                when surveyfield.cover_crop_species_5 = 'BARLEY' then 'barley'
                when surveyfield.cover_crop_species_5 = 'BERSEEM_CLOVER' then 'berseem clover'
                when surveyfield.cover_crop_species_5 = 'BUCKWHEAT' then 'buckwheat'

                when surveyfield.cover_crop_species_5 = 'CANOLA' then 'canola/rapeseed'
                when surveyfield.cover_crop_species_5 = 'CEREAL_RYE' then 'cereal (winter) rye'
                when surveyfield.cover_crop_species_5 = 'COWPEA' then 'cowpea'
                when surveyfield.cover_crop_species_5 = 'CRIMSON_CLOVER' then 'crimson clover'
                when surveyfield.cover_crop_species_5 = 'DUTCH_WHITE_CLOVER' then 'Dutch white clover'

                when surveyfield.cover_crop_species_5 = 'FIELD_PEA' then 'field/forage pea'
                when surveyfield.cover_crop_species_5 = 'FLAX' then 'flax'
                when surveyfield.cover_crop_species_5 = 'HAIRY_VETCH' then 'hairy vetch'
                when surveyfield.cover_crop_species_5 = 'KALE' then 'kale'
                when surveyfield.cover_crop_species_5 = 'MILLET' then 'millet'

                when surveyfield.cover_crop_species_5 = 'OATS' then 'oats'
                when surveyfield.cover_crop_species_5 = 'OTHER_LEGUME' then 'other (legume)'
                when surveyfield.cover_crop_species_5 = 'OTHER_GRASS' then 'other (grass)'
                when surveyfield.cover_crop_species_5 = 'OTHER_BROADLEAF' then 'other (broadleaf)'
                when surveyfield.cover_crop_species_5 = 'PLANTAIN' then 'plantain'


                when surveyfield.cover_crop_species_5 = 'RADISH' then 'radish'  
                when surveyfield.cover_crop_species_5 = 'RED_CLOVER' then 'red clover'
                when surveyfield.cover_crop_species_5 = 'SORGHUM' then 'sorghum'
                when surveyfield.cover_crop_species_5 = 'SORGHUM_SUDAN' then 'sorghum-sudan'
                when surveyfield.cover_crop_species_5 = 'SOYBEANS' then 'soybeans'

                when surveyfield.cover_crop_species_5 = 'SUNFLOWER' then 'sunflower'
                when surveyfield.cover_crop_species_5 = 'SUN_HEMP' then 'sun hemp'
                when surveyfield.cover_crop_species_5 = 'TRITICALE' then 'triticale'
                when surveyfield.cover_crop_species_5 = 'TURNIP' then 'turnip'
                when surveyfield.cover_crop_species_5 = 'WHEAT_SPRING' then 'wheat (spring)'

                when surveyfield.cover_crop_species_5 = 'WHEAT_WINTER' then 'wheat (winter)'
                when surveyfield.cover_crop_species_5 = 'WINTER_PEA' then 'winter pea'
                when surveyfield.cover_crop_species_5 = 'YELLOW_SWEET_CLOVER' then 'yellow sweet clover'
                when surveyfield.cover_crop_species_5 = 'MULITSPECIES' then 'multispecies mix of 2 or more'
                when surveyfield.cover_crop_species_5 = 'OTHER' then 'other'	
            end as mod_cover_crop_species_5,
            case
                when surveyfield.cover_crop_planting_rate_1_units = 'POUNDS_ACRE' then 'lbs/acre' 
                when surveyfield.cover_crop_planting_rate_1_units = 'BUSHELS_ACRE' then 'bu/acre' 
            end as mod_cover_crop_planting_rate_1_units,	
            case
                when surveyfield.cover_crop_planting_rate_2_units = 'POUNDS_ACRE' then 'lbs/acre' 
                when surveyfield.cover_crop_planting_rate_2_units = 'BUSHELS_ACRE' then 'bu/acre' 
            end as mod_cover_crop_planting_rate_2_units,	
            case
                when surveyfield.cover_crop_planting_rate_3_units = 'POUNDS_ACRE' then 'lbs/acre' 
                when surveyfield.cover_crop_planting_rate_3_units = 'BUSHELS_ACRE' then 'bu/acre' 
            end as mod_cover_crop_planting_rate_3_units,	
            case
                when surveyfield.cover_crop_planting_rate_4_units = 'POUNDS_ACRE' then 'lbs/acre' 
                when surveyfield.cover_crop_planting_rate_4_units = 'BUSHELS_ACRE' then 'bu/acre' 
            end as mod_cover_crop_planting_rate_4_units,	
            case
                when surveyfield.cover_crop_planting_rate_5_units = 'POUNDS_ACRE' then 'lbs/acre' 
                when surveyfield.cover_crop_planting_rate_5_units = 'BUSHELS_ACRE' then 'bu/acre' 
            end as mod_cover_crop_planting_rate_5_units
            , case	        
                when surveyfield.tillage_system_cash_crop  = 'CONVENTIONAL' then 'conventional tillage (<15% residue)'
                when surveyfield.tillage_system_cash_crop = 'REDUCED' then 'reduced tillage (15-30% residue)'
                when surveyfield.tillage_system_cash_crop = 'MULCH_TILL' then 
                    'conservation tillage (>30% residue) - mulch till/vertical tillage'
                when surveyfield.tillage_system_cash_crop = 'STRIP_TILL' then 'conservation tillage (>30% residue) - strip till'
                when surveyfield.tillage_system_cash_crop = 'NO_TILL' then 'conservation tillage (>30% residue) - no till'    
            end as mod_tillage_system_cash_crop
            , case	        
                when surveyfield.tillage_system_cash_crop = 'CONVENTIONAL' then 'Conventional, <15% residue remaining'
                when surveyfield.tillage_system_cash_crop = 'REDUCED' then 'Reduced, 15-30% residue remaining'
                when surveyfield.tillage_system_cash_crop = 'MULCH_TILL' then 
                    'Conservation, >30% residue remaining'
                when surveyfield.tillage_system_cash_crop = 'STRIP_TILL' then 'Conservation, >30% residue remaining'
                when surveyfield.tillage_system_cash_crop = 'NO_TILL' then 'Conservation, >30% residue remaining'    
            end as mod_residue_remaining
            , case 
                when surveyfield.cover_crop_seeding_method = 'FROST' then'frost seeded'
                when surveyfield.cover_crop_seeding_method = 'DRILLED' then 'drilled'
                when surveyfield.cover_crop_seeding_method = 'BROADCAST_NO_INCORP' then 'broadcast, no incorporation'
                when surveyfield.cover_crop_seeding_method = 'EARLY_INTERSEED' then 'early interseeded -- broadcast'
                when surveyfield.cover_crop_seeding_method = 'LATE_INTERSEED_BROADCAST' then 'late interseeded -- broadcast'
                when surveyfield.cover_crop_seeding_method = 'LATE_INTERSEED_AERIAL' then 'late interseeded -- aerial'
                when surveyfield.cover_crop_seeding_method = 'BROADCAST_INCORPORATION' then 'broadcast + incorporation'
                when surveyfield.cover_crop_seeding_method = 'FERT_BROADCAST_INCORP' then 'cover crop seed mixed with fertilizer + broadcast + incorporation'
                when surveyfield.cover_crop_seeding_method = 'OTHER' then 'other'
            end as mod_cc_seeding_method
            , case 
                when surveyfield.manure_prior_rate_units = 'GALLONS' then 'gal/acre'
                when surveyfield.manure_prior_rate_units = 'POUNDS_ACRE' then 'lbs/acre'
            end as mod_manure_prior_rate_units
            , case 
                when surveyfield.manure_post_rate_units = 'GALLONS' then 'gal/acre'
                when surveyfield.manure_post_rate_units = 'POUNDS_ACRE' then 'lbs/acre'
            end as mod_manure_post_rate_units
            , case 
                when surveyfield.cover_crop_estimated_termination = 'GRAZE_FALL' then 'graze fall'
                when surveyfield.cover_crop_estimated_termination = 'WINTERKILL' then 'little to no cover crop growth in spring'
                when surveyfield.cover_crop_estimated_termination = 'FALLKILL' then 'killing frost (fall)'
                when surveyfield.cover_crop_estimated_termination = 'GRAZE_SPRING' then 'graze spring'
                when surveyfield.cover_crop_estimated_termination = 'SPRING_HERBICIDE' then 'early spring, herbicide application (14 plus days prior to crop establishment)'
                
                when surveyfield.cover_crop_estimated_termination = 'FORAGE' then 'harvest for forage'
                when surveyfield.cover_crop_estimated_termination = 'GREEN_HERBICIDE' then 'plant green, herbicide termination'
                when surveyfield.cover_crop_estimated_termination = 'SPRING_ROLLER_CRIMPER' then 'early spring, roller-crimper termination'
                when surveyfield.cover_crop_estimated_termination = 'GREEN_ROLLER_CRIMPER' then 'plant green, roller-crimper termination'
                when surveyfield.cover_crop_estimated_termination = 'OTHER' then 'other'
            end as mod_cover_crop_estimated_termination,
            case 
                when surveyfield.crop_rotation_2023_cash_crop_species = 'CORN_FOR_GRAIN' then 'corn for grain'
                when surveyfield.crop_rotation_2023_cash_crop_species = 'CORN_SILAGE' then 'corn silage'
                when surveyfield.crop_rotation_2023_cash_crop_species = 'SOYBEANS' then 'soybeans'
                when surveyfield.crop_rotation_2023_cash_crop_species = 'WHEAT' then 'wheat'
                when surveyfield.crop_rotation_2023_cash_crop_species = 'OATS' then 'oats'
                when surveyfield.crop_rotation_2023_cash_crop_species = 'BARLEY' then 'barley'
                when surveyfield.crop_rotation_2023_cash_crop_species = 'TRITICALE' then 'triticale'
                when surveyfield.crop_rotation_2023_cash_crop_species = 'SORGHUM' then 'sorghum'
                when surveyfield.crop_rotation_2023_cash_crop_species = 'SORGHUM_SUDAN' then 'sorghum-sudan'
                when surveyfield.crop_rotation_2023_cash_crop_species = 'ALFALFA' then 'alfalfa'
                when surveyfield.crop_rotation_2023_cash_crop_species = 'VEGETABLE_CROP' then 'vegetable crop'
                when surveyfield.crop_rotation_2023_cash_crop_species = 'OTHER_GRAIN' then 'other grain'
                when surveyfield.crop_rotation_2023_cash_crop_species = 'OTHER_FORAGE' then 'other forage'
                when surveyfield.crop_rotation_2023_cash_crop_species = 'LIVESTOCK' then 'livestock feeding/grazing'	   	
            end as mod_crop_rotation_2023_cash_crop_species
            
			from wisccc_surveyfarm as surveyfarm
			left join wisccc_surveyfield as surveyfield
			on surveyfarm.id = surveyfield.survey_farm_id
			left join (
                select 
                    wff.id,
                    wff.closest_zip_code,
                    wff.field_acreage,
                    wff.derived_county,
                    wff.farmer_id,
                    ST_GeometryN(ST_GeneratePoints(wff.b_field_location, 1), 1) as field_location
                from (
                    select *, st_buffer(field_location, 0.045) as b_field_location
                    from wisccc_fieldfarm                
                ) as wff
            ) as fieldfarm
			on surveyfield.field_farm_id = fieldfarm.id
			left join wisccc_ancillarydata as ancil
			on surveyfield.id = ancil.survey_field_id  
			left join wisccc_farmer as farmer
			on surveyfarm.farmer_id = farmer.id
			where surveyfarm.survey_year >= 2023
                and surveyfarm.confirmed_accurate = TRUE
	) as a
	
    """

    if f_output == "sql":
        return query

    if f_output == "json":
        query_json = """
            SELECT jsonb_build_object(
                'type',     'FeatureCollection',
                'features', jsonb_agg(features.feature)
            )
            FROM (
            SELECT jsonb_build_object(
                'type',       'Feature',
                'id',         id,
                'geometry',   ST_AsGeoJSON(farmlocation)::jsonb,
                'properties', to_jsonb(inputs) - 'id' - 'farmlocation'
            ) AS feature
            FROM (
                    select
                        *, 
                        ST_SetSRID(ST_MakePoint(site_lon, site_lat), 4326) as farmlocation
                    from (
                        {query}
                        ) as b
                ) as inputs
            ) features;""".format(
            query=query
        )

        with connection.cursor() as cursor:
            cursor.execute(query_json)
            rows = cursor.fetchone()
            data = json.loads(rows[0])

        return data

    if f_output == "table":
        table_name = "wisc_cc_all_together"
        with connection.cursor() as cursor:
            try:
                cursor.execute(f"drop table {table_name};")
            except:
                print(f"{table_name} currently does not exist.")

            print(f"Creating {table_name}")
            cursor.execute(
                """
            create table {table_name} as
                           {query}
        """.format(
                    table_name=table_name, query=query
                )
            )

    if f_output == "df":
        data = pd.read_sql(query, connection)
        # df.value_counts(['cc_species', 'cc_species_raw'])
        return data


def data_export():
    """For exporting an Excel doc for collaborating researchers"""

    df = pull_all_years_together("df")
    df = df.drop(
        columns=[
            "survey_response_id",
            "id",
            "farm_id",
            "years_experience",
            "anpp",
            "days_from_plant_to_bio_hrvst",
            "cc_rate_and_species",
            "cc_species",
            "tillage_system",
        ]
    )
    df = df.rename(
        columns={
            "survey_field_id": "field_id",
            "year": "survey_year",
            "county": "county_farm",
            "county_single": "county_field",
            "cc_termination": "cc_termination_timing_method",
            "cc_biomass_collection_date": "cc_biomass_collection_date_fall",
            "total_precip": "total_precip_fall",
            "acc_gdd": "acc_gdd_fall",
            "cc_biomass": "cc_biomass_fall",
            "fq_cp": "fq_cp_fall",
            "fq_andf": "fq_andf_fall",
            "fq_undfom30": "fq_undfom30_fall",
            "fq_ndfd30": "fq_ndfd30_fall",
            "fq_tdn_adf": "fq_tdn_adf_fall",
            "fq_milkton": "fq_milkton_fall",
            "fq_rfq": "fq_rfq_fall",
            "fq_undfom240": "fq_undfom240_fall",
            "fq_dry_matter": "fq_dry_matter_fall",
            "fq_adf": "fq_adf_fall",
            "fq_rfv": "fq_rfv_fall",
            "total_nitrogen": "percent_nitrogen_fall",

            "percent_p":"percent_p_fall",
            "percent_k":"percent_k_fall",
            "percent_ca":"percent_ca_fall",
            "percent_mg":"percent_mg_fall",
            "percent_s":"percent_s_fall",
            "c_to_n_ratio":"c_to_n_ratio_fall",

            "n_content":"n_lbs_acre_fall",
            "p_content":"p_lbs_acre_fall",
            "k_content":"k_lbs_acre_fall",
            "ca_content":"ca_lbs_acre_fall",
            "mg_content":"mg_lbs_acre_fall",
            "s_content":"s_lbs_acre_fall",
            "c_content":"c_lbs_acre_fall",

            "height_of_stand": "height_of_stand_fall",
            "fall_notes": "notes_fall",
            "spring_cc_biomass_collection_date": "cc_biomass_collection_date_spring",
            "spring_total_precip": "total_precip_spring",
            "spring_acc_gdd": "acc_gdd_spring",
            "spring_cc_biomass": "cc_biomass_spring",
            "spring_fq_cp": "fq_cp_spring",
            "spring_fq_andf": "fq_andf_spring",
            "spring_fq_undfom30": "fq_undfom30_spring",
            "spring_fq_ndfd30": "fq_ndfd30_spring",
            "spring_fq_tdn_adf": "fq_tdn_adf_spring",
            "spring_fq_milkton": "fq_milkton_spring",
            "spring_fq_rfq": "fq_rfq_spring",
            "spring_fq_undfom240": "fq_undfom240_spring",
            "spring_fq_dry_matter": "fq_dry_matter_spring",
            "spring_fq_adf": "fq_adf_spring",
            "spring_fq_rfv": "fq_rfv_spring",
            "spring_total_nitrogen": "percent_nitrogen_spring",
            
            "spring_percent_p":"percent_p_spring",
            "spring_percent_k":"percent_k_spring",
            "spring_percent_ca":"percent_ca_spring",
            "spring_percent_mg":"percent_mg_spring",
            "spring_percent_s":"percent_s_spring",
            "spring_c_to_n_ratio":"c_to_n_ratio_spring",

            "spring_n_content":"n_lbs_acre_spring",
            "spring_p_content":"p_lbs_acre_spring",
            "spring_k_content":"k_lbs_acre_spring",
            "spring_ca_content":"ca_lbs_acre_spring",
            "spring_mg_content":"mg_lbs_acre_spring",
            "spring_s_content":"s_lbs_acre_spring",
            "spring_c_content":"c_lbs_acre_spring",
            
            "spring_height_of_stand": "height_of_stand_spring",
            "spring_notes": "notes_spring",
        }
    )

    # Excel doesn't want datetimes with timezones, so converting
    # to dates
    cols_wtzs = [
        "cash_crop_planting_date",
        "cc_planting_date",
        "cc_biomass_collection_date_fall",
        "cc_biomass_collection_date_spring",
    ]
    for col_wtz in cols_wtzs:
        try:
            df[col_wtz] = df[col_wtz].apply(lambda a: pd.to_datetime(a).date())
        except AttributeError:
            df[col_wtz] = df[col_wtz].where(~pd.isnull(df[col_wtz]), other=pd.NaT)
            df[col_wtz] = df[col_wtz].apply(lambda a: pd.to_datetime(a).date())

    # Surveys before 2023 have periods (".") for nulls,
    #   this will clean them up.
    # Currently replacing with blank
    cols_wperiods = [
        "tillage_equip_primary",
        "tillage_equip_secondary",
        "cc_planting_rate",
        "cc_termination_timing_method",
    ]
    for col_wperiod in cols_wperiods:
        df[col_wperiod] = df[col_wperiod].replace(".", "")

    file_dat = "data/cover_crop_data_export_wmetadata.csv"
    file_dat = os.path.join(settings.BASE_DIR, file_dat)

    metadata = pd.read_csv(file_dat, sep="\t")
    from io import BytesIO, StringIO

    output = BytesIO()
    # response = HttpResponse(content_type="application/ms-excel")
    writer = pd.ExcelWriter(output, engine="xlsxwriter")
    # writer = pd.ExcelWriter(
    #     excelfile, engine="openpyxl", mode="a", if_sheet_exists="replace"
    # )

    # writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
    metadata.to_excel(writer, sheet_name="Metadata", index=False)
    df.to_excel(writer, sheet_name="Wisconsin Cover Crop Data", index=False)
    writer.close()

    return output.getvalue()


def export_agronomic_data():
    export_name = "wisc_cc_data_export_{}.xlsx".format(
        datetime.datetime.now().strftime("%Y_%m_%d")
    )
    excel_bytes = data_export()
    print(type(excel_bytes))
    response = HttpResponse(excel_bytes, content_type="application/ms-excel")
    response["Content-Disposition"] = f"attachment; filename={export_name}"

    return response
