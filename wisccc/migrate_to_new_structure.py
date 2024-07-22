from django.db import connection
from django.contrib.auth.models import User
from wisccc.models import (
    Survey,
    SurveyFarm,
    SurveyField,
    SurveyPhoto,
    AncillaryData,
    FieldFarm,
    Farmer,
)


def grab_ancillary_data(survey_id, prop):
    """For grabbing ancillary data for 2023"""
    if prop == "biomass_collection_date":
        query = f"""
                select COALESCE(
                        TO_DATE(date_reported_biomass,'YYYY-MM-DD'),
                        TO_DATE(date_processed,'YYYY-MM-DD')
                    ) as cc_biomass_collection_date
                from all_lab_data_2023
                where id = '{survey_id}'
                """
    else:
        query = f"""
                select {prop}
                from all_lab_data_2023
                where id = '{survey_id}'
                """
    with connection.cursor() as cursor:
        cursor.execute(query)

        rslt = cursor.fetchone()

        try:
            val = rslt[0]
        except:
            val = None
        return val


def migrate_to_new_structure():
    surveys = Survey.objects.all()

    for survey in surveys:
        print(survey.id)
        user = survey.user
        try:
            farmer = Farmer.objects.get(user_id=user.id)
        except:
            continue
        print("Migrating to survey farm...")
        if survey.survey_year is None:
            survey.survey_year = 2023
        survey_farm = SurveyFarm.objects.create(
            survey_year=survey.survey_year,
            notes_admin=survey.notes_admin,
            confirmed_accurate=survey.confirmed_accurate,
            years_experience=survey.years_experience,
            total_acres=survey.total_acres,
            percent_of_farm_cc=survey.percent_of_farm_cc,
            dominant_soil_series_1=survey.dominant_soil_series_1,
            dominant_soil_series_2=survey.dominant_soil_series_2,
            dominant_soil_series_3=survey.dominant_soil_series_3,
            dominant_soil_series_4=survey.dominant_soil_series_4,
            info_source_nutrient_mgmt_1=survey.info_source_nutrient_mgmt_1,
            info_source_nutrient_mgmt_2=survey.info_source_nutrient_mgmt_2,
            info_source_nutrient_mgmt_3=survey.info_source_nutrient_mgmt_3,
            source_nutrient_mgmt_write_in=survey.source_nutrient_mgmt_write_in,
            cov_crops_for_ntrnt_mgmt_comments_questions=survey.cov_crops_for_ntrnt_mgmt_comments_questions,
            info_source_cover_crops_1=survey.info_source_cover_crops_2,
            info_source_cover_crops_2=survey.info_source_cover_crops_2,
            info_source_cover_crops_3=survey.info_source_cover_crops_3,
            info_source_cover_crops_write_in=survey.info_source_cover_crops_write_in,
            support_cover_crops_1=survey.support_cover_crops_1,
            support_cover_crops_2=survey.support_cover_crops_2,
            support_cover_crops_3=survey.support_cover_crops_3,
            support_cover_crops_write_in=survey.support_cover_crops_write_in,
            lacking_any_info_cover_crops=survey.lacking_any_info_cover_crops,
            barriers_to_expansion=survey.barriers_to_expansion,
            quit_planting_cover_crops=survey.quit_planting_cover_crops,
            if_use_crop_insurance=survey.if_use_crop_insurance,
            why_cover_crops_write_in=survey.why_cover_crops_write_in,
            cover_crops_delay_cash_crop=survey.cover_crops_delay_cash_crop,
            save_cover_crop_seed=survey.save_cover_crop_seed,
            source_cover_crop_seed=survey.source_cover_crop_seed,
            interesting_tales=survey.interesting_tales,
            where_to_start=survey.where_to_start,
            additional_thoughts=survey.additional_thoughts,
            farmer=farmer,
        )
        print("Migrating to field farm...")
        field_farm = FieldFarm.objects.create(
            field_name=None,
            closest_zip_code=survey.closest_zip_code,
            field_acreage=survey.field_acreage,
            field_location=survey.farm_location,
            farmer=farmer,
            derived_county=survey.derived_county,
        )
        print("Migrating to survey field...")
        survey_field = SurveyField.objects.create(
            crop_rotation=survey.crop_rotation,
            crop_rotation_2021_cover_crop_species=survey.crop_rotation_2021_cover_crop_species,
            crop_rotation_2021_cash_crop_species=survey.crop_rotation_2021_cash_crop_species,
            crop_rotation_2022_cover_crop_species=survey.crop_rotation_2022_cover_crop_species,
            crop_rotation_2022_cash_crop_species=survey.crop_rotation_2022_cash_crop_species,
            crop_rotation_2023_cover_crop_species=survey.crop_rotation_2023_cover_crop_species,
            crop_rotation_2023_cash_crop_species=survey.crop_rotation_2023_cash_crop_species,
            cover_crop_species_1=survey.cover_crop_species_1,
            cover_crop_planting_rate_1=survey.cover_crop_planting_rate_1,
            cover_crop_planting_rate_1_units=survey.cover_crop_planting_rate_1_units,
            cover_crop_species_2=survey.cover_crop_species_2,
            cover_crop_planting_rate_2=survey.cover_crop_planting_rate_2,
            cover_crop_planting_rate_2_units=survey.cover_crop_planting_rate_2_units,
            cover_crop_species_3=survey.cover_crop_species_3,
            cover_crop_planting_rate_3=survey.cover_crop_planting_rate_3,
            cover_crop_planting_rate_3_units=survey.cover_crop_planting_rate_3_units,
            cover_crop_species_4=survey.cover_crop_species_4,
            cover_crop_planting_rate_4=survey.cover_crop_planting_rate_4,
            cover_crop_planting_rate_4_units=survey.cover_crop_planting_rate_4_units,
            cover_crop_species_5=survey.cover_crop_species_5,
            cover_crop_planting_rate_5=survey.cover_crop_planting_rate_5,
            cover_crop_planting_rate_5_units=survey.cover_crop_planting_rate_5_units,
            cover_crop_species_and_rate_write_in=survey.cover_crop_species_and_rate_write_in,
            cover_crop_multispecies_mix_write_in=survey.cover_crop_multispecies_mix_write_in,
            cash_crop_planting_date=survey.cash_crop_planting_date,
            years_with_cover_crops=survey.years_with_cover_crops,
            dominant_soil_texture=survey.dominant_soil_texture,
            manure_prior=survey.manure_prior,
            manure_prior_rate=survey.manure_prior_rate,
            manure_prior_rate_units=survey.manure_prior_rate_units,
            manure_post=survey.manure_post,
            manure_post_rate=survey.manure_post_rate,
            manure_post_rate_units=survey.manure_post_rate_units,
            tillage_system_cash_crop=survey.tillage_system_cash_crop,
            primary_tillage_equipment=survey.primary_tillage_equipment,
            primary_tillage_equipment_write_in=survey.primary_tillage_equipment_write_in,
            secondary_tillage_equipment=survey.secondary_tillage_equipment,
            secondary_tillage_equipment_write_in=survey.secondary_tillage_equipment_write_in,
            soil_conditions_at_cover_crop_seeding=survey.soil_conditions_at_cover_crop_seeding,
            cover_crop_seeding_method=survey.cover_crop_seeding_method,
            cover_crop_seeding_method_write_in=survey.cover_crop_seeding_method_write_in,
            cover_crop_seed_cost=survey.cover_crop_seed_cost,
            cover_crop_planting_cost=survey.cover_crop_planting_cost,
            cover_crop_planting_date=survey.cover_crop_planting_date,
            cover_crop_estimated_termination=survey.cover_crop_estimated_termination,
            days_between_crop_hvst_and_cc_estd=survey.days_between_crop_hvst_and_cc_estd,
            derived_species_class=survey.derived_species_class,
            field_farm=field_farm,
            survey_farm=survey_farm,
        )
        print("Updating survey field in ancillary data...")
        try:
            # If records exists (which will be 2020-2022)
            # Grab it, then add the surveyfield rather than response
            ancillary_data = AncillaryData.objects.get(survey_response_id=survey.id)
            ancillary_data.survey_field = survey_field
            ancillary_data.save()
        except:
            ancillary_data = AncillaryData.objects.create(
                biomass_collection_date=grab_ancillary_data(
                    survey.id, "biomass_collection_date"
                ),
                cp=grab_ancillary_data(survey.id, "cp"),
                andf=grab_ancillary_data(survey.id, "andf"),
                undfom30=grab_ancillary_data(survey.id, "undfom30"),
                ndfd30=grab_ancillary_data(survey.id, "ndfd30"),
                tdn_adf=grab_ancillary_data(survey.id, "tdn_adf"),
                milk_ton_milk2013=grab_ancillary_data(survey.id, "milk_ton_milk2013"),
                rfq=grab_ancillary_data(survey.id, "rfq"),
                cc_biomass=grab_ancillary_data(survey.id, "cc_biomass"),
                total_nitrogen=grab_ancillary_data(survey.id, "total_nitrogen"),
                acc_gdd=None,
                total_precip=None,
                spring_biomass_collection_date=None,
                spring_cc_biomass=None,
                survey_response=survey,
                survey_field=survey_field,
            )
        print("Updating survey field in survey photo...")
        try:
            print("Trying to grab a photo...")
            survey_photo = SurveyPhoto.objects.get(survey_response_id=survey.id)
            survey_photo.survey_field = survey_field
            survey_photo.save()
        except:
            print("No photo.")


def update_jerry_daniels():
    """for updating jerry daniels three surveys
    Arbitrarily assigning his surveys and fields to the first farmer
    entry for him.
    Double check these ids in prod"""
    jd_farm = Farmer.objects.get(id=47)
    jd_survey_farms = SurveyFarm.objects.filter(farmer__in=[47, 48, 49, 50])
    jd_field_farms = FieldFarm.objects.filter(farmer__in=[47, 48, 49, 50])
    for jd_survey_farm in jd_survey_farms:
        jd_survey_farm.farmer = jd_farm

    for jd_field_farm in jd_field_farms:
        jd_field_farm.farmer = jd_farm
