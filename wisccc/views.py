from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
import json
import djqscsv
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from wisccc.forms import SurveyForm1, SurveyForm2, SurveyForm3, FarmerForm
from wisccc.models import Survey, Farmer
import pandas as pd


def check_section_completed(user_id, section):
    """Checks a particular section, farmer, 1, 2, 3
    to see if a particualr required field is a completed."""

    if section == "farmer":
        farmer = Farmer.objects.filter(user_id=user_id).first()
        if farmer is None:
            return False
        if farmer.last_name == "" or farmer.last_name is None:
            return False

        return True

    if section == 1:
        survey = Survey.objects.filter(user_id=user_id).first()
        if survey is None:
            return False
        if survey.percent_of_farm_cc is None:
            return False

        return True

    if section == 2:
        survey = Survey.objects.filter(user_id=user_id).first()
        if survey is None:
            return False
        if survey.farm_location is None:
            return False

        return True

    if section == 3:
        survey = Survey.objects.filter(user_id=user_id).first()
        if survey is None:
            return False
        if survey.additional_thoughts is None:
            return False

        return True


def get_survey_data():
    """For getting survey data and returning an excel doc"""
    query = """
        select 
            s.id
            , f.first_name 
            , f.last_name	
            , f.farm_name  
            , f.county 
            , s.years_experience
            , s.total_acres
            , s.percent_of_farm_cc
            , s.dominant_soil_series_1
            , s.dominant_soil_series_2
            , s.dominant_soil_series_3
            , s.dominant_soil_series_4
            , s.info_source_nutrient_mgmt_1
            , s.info_source_nutrient_mgmt_2
            , s.info_source_nutrient_mgmt_3
            , s.source_nutrient_mgmt_write_in
            , s.cov_crops_for_ntrnt_mgmt_comments_questions
            , s.info_source_cover_crops_1
            , s.info_source_cover_crops_2
            , s.info_source_cover_crops_3
            , s.info_source_cover_crops_write_in
            , s.info_source_cover_crops_social_media
            , s.support_cover_crops_1
            , s.support_cover_crops_2
            , s.support_cover_crops_3
            , s.support_cover_crops_write_in
            , s.lacking_any_info_cover_crops
            , s.like_to_expand_cover_crops
            , s.barriers_to_expansion
            , s.top_risks_of_cover_cropping_mgmt
            , s.quit_planting_cover_crops
            , s.use_crop_insurance
            , s.if_use_crop_insurance
            , s.why_cover_crops_1
            , s.why_cover_crops_2
            , s.why_cover_crops_3
            , s.why_cover_crops_4
            , s.why_cover_crops_write_in
            , s.cover_crops_delay_cash_crop
            , s.save_cover_crop_seed
            , s.source_cover_crop_seed
            , s.closest_zip_code
            , s.field_acreage
            , s.crop_rotation
            , s.crop_rotation_2021_cover_crop_species
            , s.crop_rotation_2021_cash_crop_species
            , s.crop_rotation_2022_cover_crop_species
            , s.crop_rotation_2022_cash_crop_species
            , s.crop_rotation_2023_cover_crop_species
            , s.crop_rotation_2023_cash_crop_species
            , s.cover_crop_species_1
            , s.cover_crop_planting_rate_1
            , s.cover_crop_species_2
            , s.cover_crop_planting_rate_2
            , s.cover_crop_species_3
            , s.cover_crop_planting_rate_3
            , s.cover_crop_species_4
            , s.cover_crop_planting_rate_4
            , s.cover_crop_species_5
            , s.cover_crop_planting_rate_5
            , s.cover_crop_species_and_rate_write_in
            , s.previous_crop
            , s.cash_crop_planting_date
            , s.years_with_cover_crops
            , s.dominant_soil_texture
            , s.manure_prior
            , s.manure_prior_rate
            , s.manure_prior_rate_units
            , s.manure_post
            , s.manure_post_rate
            , s.manure_post_rate_units
            , s.tillage_system_cash_crop
            , s.primary_tillage_equipment_1
            , s.primary_tillage_equipment_2
            , s.primary_tillage_equipment_write_in
            , s.secondary_tillage_equipment
            , s.secondary_tillage_equipment_write_in
            , s.soil_conditions_at_cover_crop_seeding
            , s.cover_crop_seeding_method
            , s.cover_crop_seeding_method_write_in
            , s.cover_crop_seed_cost
            , s.cover_crop_planting_cost
            , s.cover_crop_planting_date
            , s.cover_crop_estimated_termination
            , s.days_between_crop_hvst_and_cc_estd
            , s.interesting_tales
            , s.where_to_start
            , s.additional_thoughts
            , s.user_id
            , st_x( farm_location ) as longitude
            , st_y( farm_location ) as latitude
            , s.last_updated
            , s.survey_created
        from wisccc_survey s 
        left join wisccc_farmer f
        on s.user_id = f.user_id """
    dat = pd.read_sql(query, connection)
    return dat


def wisc_cc_home(request):
    return render(request, "wisccc/wisc_cc_home.html")


# @permission_required("wisccc.survery_manager", raise_exception=True)
def wisccc_download_data(request):
    # qs = Survey.objects.raw(query)
    # return djqscsv.render_to_csv_response(qs)
    df = get_survey_data()
    resp = HttpResponse(content_type="text/csv")
    resp["Content-Disposition"] = "attachment; filename=survey_data.csv"

    df.to_csv(path_or_buf=resp, sep=",", index=False)
    return resp


@login_required
def wisc_cc_survey(request):
    """Home page for Cover Crop survey. We check progress of different sections of the survey
    by querying one required question from each section (0 (the farmer section),1,2,3).
    If this is completed then we assume it is all completed."""
    completed_0 = check_section_completed(request.user.id, "farmer")
    completed_1 = check_section_completed(request.user.id, 1)
    completed_2 = check_section_completed(request.user.id, 2)
    completed_3 = check_section_completed(request.user.id, 3)

    template = "wisccc/wisc_cc_survey.html"

    return render(
        request,
        template,
        {
            "completed_0": completed_0,
            "completed_1": completed_1,
            "completed_2": completed_2,
            "completed_3": completed_3,
        },
    )


@login_required
def wisc_cc_survey0(request):
    try:
        instance = Farmer.objects.filter(user_id=request.user.id).first()
    except:
        instance = Farmer.objects.create(user_id=request.user.id)

    form = FarmerForm(request.POST or None, instance=instance)
    if form.is_valid():
        new_form = form.save(commit=False)
        new_form.user = request.user
        new_form.save()

        return redirect("wisc_cc_survey")

    # template = "wisccc/survey_upload_all.html"
    template = "wisccc/survey_section_0.html"
    return render(
        request,
        template,
        {
            "form": form,
        },
    )


@login_required
def wisc_cc_survey1(request):
    try:
        instance = Survey.objects.filter(user_id=request.user.id).earliest(
            "last_updated"
        )
    except:
        instance = Survey.objects.create(user_id=request.user.id)

    form = SurveyForm1(request.POST or None, instance=instance)
    if form.is_valid():
        new_form = form.save(commit=False)
        new_form.user = request.user
        new_form.save()

        return redirect("wisc_cc_survey2")

    # template = "wisccc/survey_upload_all.html"
    template = "wisccc/survey_section_1.html"
    return render(
        request,
        template,
        {
            "form": form,
        },
    )


@login_required
def wisc_cc_survey2(request):
    try:
        instance = Survey.objects.filter(user_id=request.user.id).earliest(
            "last_updated"
        )
    except:
        instance = Survey.objects.create(user_id=request.user.id)

    form = SurveyForm2(request.POST or None, instance=instance)

    if form.is_valid():
        new_form = form.save(commit=False)
        new_form.user = request.user
        new_form.save()

        return redirect("wisc_cc_survey3")

    template = "wisccc/survey_section_2.html"
    return render(
        request,
        template,
        {
            "form": form,
        },
    )


@login_required
def wisc_cc_survey3(request):
    try:
        instance = Survey.objects.filter(user_id=request.user.id).earliest(
            "last_updated"
        )
    except:
        instance = Survey.objects.create(user_id=request.user.id)

    form = SurveyForm3(request.POST or None, instance=instance)

    if form.is_valid():
        new_form = form.save(commit=False)
        new_form.user = request.user
        new_form.save()

        return redirect("wisc_cc_survey")

    template = "wisccc/survey_section_3.html"
    return render(
        request,
        template,
        {
            "form": form,
        },
    )


def wisc_cc_graph(request):
    return render(request, "wisccc/wisc_cc_graph.html")


def wisc_cc_map(request):
    return render(request, "wisccc/wisc_cc_map_toggle.html")


def wisc_cc_map_v2(request):
    return render(request, "wisccc/wisc_cc_map_toggle.html")


@xframe_options_exempt
def wisc_cc_map_embed(request):
    return render(request, "wisccc/wisc_cc_map_embed.html")


def get_wi_counties(request):
    # from django.db import connection

    def get_county_json():
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT jsonb_build_object(
                    'type',     'FeatureCollection',
                    'features', jsonb_agg(features.feature)
                )
                FROM (
                  SELECT jsonb_build_object(
                    'type',       'Feature',
                    'id',         id,
                    'geometry',   ST_AsGeoJSON(geom)::jsonb,
                    'properties', to_jsonb(inputs) - 'geom' - 'id'
                  ) AS feature
                  FROM (
                    SELECT 
                            objectid as id 
                            , countyname
                            , shape as geom
                            from wi_counties
                    ) as inputs
                ) features;
            """
            )
            rows = cursor.fetchone()
            data = json.loads(rows[0])
        return data

    data = get_county_json()

    return JsonResponse(data, safe=False)


# For accessing data from previous years survey
def wisc_cc_static_data(request):
    def get_json():
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT jsonb_build_object(
                    'type',     'FeatureCollection',
                    'features', jsonb_agg(features.feature)
                )
                FROM (
                  SELECT jsonb_build_object(
                    'type',       'Feature',
                    'id',         id,
                    'geometry',   ST_AsGeoJSON(collectionpoint)::jsonb,
                    'properties', to_jsonb(inputs) - 'id' - 'collectionpoint'
                  ) AS feature
                  FROM (
                    SELECT 
                            geom.id
                            , geom.year
                            , geom.county
                            , geom.county_single
                            , geom.years_experience
                            , geom.zipcode
                            , geom.previous_crop
                            , geom.cash_crop_planting_date 
                            , geom.dominant_soil_texture
                            , geom.manure_prior 
                            , geom.manure_post
                            , geom.manure_rate 
                            , geom.manure_value 
                            , geom.tillage_system 
                            , geom.tillage_equip_primary
                            , geom.tillage_equip_secondary
                            , geom.residue_remaining
                            , geom.soil_conditions
                            , geom.cc_seeding_method
                            , geom.cc_planting_rate
                            , geom.cc_termination
                            , geom.days_between_crop_hvst_and_cc_estd
                            , geom.cc_planting_date
                            , geom.anpp
                            , geom.cc_biomass_collection_date
                            , geom.total_precip
                            , geom.acc_gdd
                            , geom.days_from_plant_to_bio_hrvst
                            , geom.cc_biomass
                            , geom.fq_cp
                            , geom.fq_andf
                            , geom.fq_undfom30
                            , geom.fq_ndfd30
                            , geom.fq_tdn_adf
                            , geom.fq_milkton
                            , geom.fq_rfq
                            , geom.cc_rate_and_species
                            , geom.cc_species
                            , ST_GeometryN(ST_GeneratePoints(geom.b_collectionpoint, 1), 1) as collectionpoint 
                        FROM (
                            select 
                                *, ST_Buffer(ST_SetSRID(ST_MakePoint(site_lon, site_lat), 4326), 0.02) as b_collectionpoint
                                from wisc_cc wc
                            ) AS geom
                    ) as inputs) features;
            """
            )
            rows = cursor.fetchone()
            data = json.loads(rows[0])
        return data

    data = get_json()

    return JsonResponse(list(data["features"]), safe=False)
